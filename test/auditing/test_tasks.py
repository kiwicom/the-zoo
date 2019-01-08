import pytest
from contextlib import contextmanager

import arrow
from factory import Faker

from zoo.auditing import tasks as uut
from zoo.auditing.check_discovery import KINDS
from zoo.auditing.models import Issue
from zoo.repos.models import Provider

pytestmark = pytest.mark.django_db


@contextmanager
def kinds(*list_of_kinds):
    for kind in list_of_kinds:
        KINDS[kind.id] = kind
    try:
        yield
    finally:
        # remove the kind from global variable KINDS
        for kind in list_of_kinds:
            KINDS.pop(kind.id, None)


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


def test_cleanup_issues__deleted_kind(repository, issue_factory, kind_factory):
    kind_1, kind_2 = kind_factory(), kind_factory()
    issue_1, _ = (
        issue_factory(repository=repository, kind_key=kind_1.id),
        issue_factory(repository=repository, kind_key=kind_2.id),
    )

    with kinds(kind_1):
        uut.cleanup_issues()

    # issue_1 should still exist while issue_2 should be deleted by cleanup_issues
    # as the kind_2 has never been registered in the KINDS variable
    assert Issue.objects.filter(kind_key=kind_1.id).first().id == issue_1.id
    assert Issue.objects.filter(kind_key=kind_2.id).first() is None


def test_cleanup_issues__old_issues(repository_factory, issue_factory, kind_factory):
    kind_1, kind_2 = kind_factory(), kind_factory()
    repo_1, repo_2, repo_3 = (
        repository_factory(),
        repository_factory(),
        repository_factory(),
    )

    now = arrow.utcnow().datetime
    one_hour_ago = arrow.utcnow().shift(hours=-1).datetime
    three_hours_ago = arrow.utcnow().shift(hours=-3).datetime

    issues = [
        issue_factory(repository=repo, kind_key=kind_1.id, last_check=last_check)
        for repo, last_check in [
            (repo_1, now),
            (repo_2, one_hour_ago),
            (repo_3, three_hours_ago),
        ]
    ] + [issue_factory(repository=repo_1, kind_key=kind_2.id, last_check=one_hour_ago)]

    with kinds(kind_1, kind_2):
        uut.cleanup_issues()

    found_issues = {issue.id for issue in Issue.objects.all()}
    assert {issues[0].id, issues[1].id, issues[3].id} == found_issues
