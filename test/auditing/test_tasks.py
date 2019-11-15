import arrow
import pytest
from factory import Faker

from zoo.auditing import tasks as uut
from zoo.auditing.models import Issue
from zoo.repos.models import Provider

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("repository__provider", [item.value for item in Provider])
def test_open_git_issues(mocker, repository, issue_factory):
    issue_1, name_1, url_1 = (
        issue_factory(repository=repository),
        Faker("user_name"),
        Faker("uri"),
    )
    issue_2, name_2, url_2 = (
        issue_factory(repository=repository),
        Faker("user_name"),
        Faker("uri"),
    )
    issues = [(issue_1.id, name_1, url_1), (issue_2.id, name_2, url_2)]
    m_create_git_issue = mocker.patch.object(uut, "create_git_issue")

    uut.bulk_create_git_issues(issues)

    m_create_git_issue.assert_has_calls(
        [mocker.call(issue_1, name_1, url_1), mocker.call(issue_2, name_2, url_2)]
    )


def test_cleanup_issues__status_unknown(
    repository, issue_factory, kind_factory, mocker
):
    kind_1, kind_2, kind_3 = kind_factory(), kind_factory(), kind_factory()

    mocker.patch("zoo.auditing.tasks.settings.ZOO_AUDITING_DROP_ISSUES", 3)

    weeks_ago = arrow.utcnow().shift(days=-5).datetime
    issue_1, issue_2, _ = (
        issue_factory(
            repository=repository,
            kind_key=kind_1.id,
            last_check=weeks_ago,
            status=Issue.Status.NEW.value,
        ),
        issue_factory(
            repository=repository,
            kind_key=kind_2.id,
            last_check=arrow.utcnow().datetime,
            deleted=True,
        ),
        issue_factory(
            repository=repository,
            last_check=weeks_ago,
            kind_key=kind_3.id,
            deleted=True,
        ),
    )

    uut.cleanup_issues()

    assert Issue.objects.get(kind_key=kind_1.id).id == issue_1.id
    assert Issue.objects.get(kind_key=kind_2.id).id == issue_2.id
    assert not Issue.objects.filter(kind_key=kind_3.id).exists()
