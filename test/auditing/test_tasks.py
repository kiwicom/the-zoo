import pytest

from factory import Faker

from zoo.auditing import tasks as uut
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
