import fakeredis
import pytest

from zoo.analytics.models import Dependency, DependencyType, DependencyUsage
from zoo.auditing.models import Issue
from zoo.repos import tasks as uut
from zoo.repos.models import Endpoint
from zoo.repos.utils import get_scm_module

from .. import dummy

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    ("repository__provider", "languages_method", "python_value"),
    [("gitlab", "languages", 100), ("github", "get_languages", 12356)],
)
def test_pull(mocker, repository, languages_method, python_value, repo_archive):
    scm_module = get_scm_module(repository.provider)
    # mock checks
    mocker.patch("zoo.repos.tasks.AUDITING_CHECKS", dummy.CHECKS)
    # mock API
    m_project = mocker.Mock(
        **{f"{languages_method}.return_value": {"Python": python_value}}
    )
    m_get_project = mocker.patch.object(
        scm_module, "get_project", return_value=m_project
    )
    m_download_archive = mocker.patch.object(
        scm_module, "download_archive", return_value=repo_archive
    )

    def redis(**kwargs):
        return fakeredis.FakeStrictRedis(**kwargs)

    mocker.patch("zoo.base.redis.get_connection", redis)

    # test
    uut.pull(repository.remote_id, repository.provider)

    # assert mocks
    getattr(m_project, languages_method).assert_called_once()

    assert m_get_project.call_args_list == [
        mocker.call(repository.remote_id),
        mocker.call(repository.remote_id),
    ]
    m_download_archive.assert_called_once_with(m_project, mocker.ANY, None)

    # assert checks / issues
    assert Issue.objects.count() == 2

    passing_issue = Issue.objects.get(kind_key="check:passing")
    assert passing_issue.repository == repository
    assert passing_issue.status == Issue.Status.NOT_FOUND.value
    assert passing_issue.details == {}

    found_issue = Issue.objects.get(kind_key="check:found")
    assert found_issue.repository == repository
    assert found_issue.status == Issue.Status.NEW.value
    assert found_issue.details == {"answer": 42}

    # assert analytics / dependencies
    assert Dependency.objects.count() == 3
    assert DependencyUsage.objects.count() == 3

    dep_usage_1 = DependencyUsage.objects.select_related("dependency").get(
        dependency__name="django"
    )
    assert dep_usage_1.dependency.type == DependencyType.PY_LIB.value
    assert dep_usage_1.repo == repository
    assert dep_usage_1.for_production is True
    assert dep_usage_1.version == "2.3.4"

    dep_usage_2 = DependencyUsage.objects.select_related("dependency").get(
        dependency__name="webpack"
    )
    assert dep_usage_2.dependency.type == DependencyType.JS_LIB.value
    assert dep_usage_2.repo == repository
    assert dep_usage_2.for_production is True
    assert dep_usage_2.version == "0.0.0-rc14"

    dep_usage_3 = DependencyUsage.objects.select_related("dependency").get(
        dependency__name="python"
    )
    assert dep_usage_3.dependency.type == DependencyType.LANG.value
    assert dep_usage_3.repo == repository
    assert dep_usage_3.for_production is None
    assert dep_usage_3.version is None

    # assert openapi
    assert Endpoint.objects.count() == 0  # the test folder is excluded by default

    mocker.patch("zoo.repos.utils.OPENAPI_SCAN_EXCLUDE", [])
    uut.pull(repository.remote_id, repository.provider)

    assert Endpoint.objects.count() == 3
    assert Endpoint.objects.filter(path="/pets").count() == 2
    assert Endpoint.objects.filter(path="/pets/{petId}").count() == 1

    endpoint = Endpoint.objects.get(path="/pets/{petId}")

    assert endpoint.repository == repository
    assert endpoint.method == "get"
    assert endpoint.operation == "showPetById"
    assert endpoint.summary == "Info for a specific pet"
