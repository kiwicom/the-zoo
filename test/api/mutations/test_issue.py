import pytest
from graphql_relay import to_global_id

from zoo.api.utils import grab
from zoo.auditing.models import Issue

pytestmark = pytest.mark.django_db


def test_wontfix(snapshot, call_api, issue_factory):
    wontfix_mutation = """
        mutation ($input: SetWontfixInput!) {
            setWontfix(input: $input) {
                issue { id status comment }
            }
        }
    """
    pk, gid, comment = 10, to_global_id(Issue.__name__, 10), "A good reason"
    issue_factory(pk=pk, status=Issue.Status.NEW.value)

    response = call_api(wontfix_mutation, input={"issueId": gid, "comment": comment})
    snapshot.assert_match(response)

    issue = grab(Issue, gid)
    assert Issue.Status(issue.status) == Issue.Status.WONTFIX
    assert issue.comment == comment
