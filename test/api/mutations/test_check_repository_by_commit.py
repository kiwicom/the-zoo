import pytest

from zoo.auditing.check_discovery import Effort, Kind, Severity
from zoo.auditing.models import Issue

pytestmark = pytest.mark.django_db


@pytest.fixture
def scenario(mocker, repository_factory, issue_factory, check_factory, fake_path):
    owner, name, sha = "games", "lemmings", "GINLNNIIJL"
    repository = repository_factory(id=42, owner=owner, name=name, remote_id=3)

    kinds = {}
    for namespace, id, status, severity, effort in [
        ("A", "new", Issue.Status.NEW, Severity.UNDEFINED, Effort.UNDEFINED),
        ("A", "fixed", Issue.Status.FIXED, Severity.ADVICE, Effort.LOW),
        ("A", "wontfix", Issue.Status.WONTFIX, Severity.WARNING, Effort.MEDIUM),
        ("A", "not-found", Issue.Status.NOT_FOUND, Severity.CRITICAL, Effort.HIGH),
        ("A", "reopened", Issue.Status.REOPENED, Severity.UNDEFINED, Effort.UNDEFINED),
        ("B", "new", Issue.Status.NEW, Severity.ADVICE, Effort.LOW),
        ("B", "fixed", Issue.Status.FIXED, Severity.WARNING, Effort.MEDIUM),
        ("B", "wontfix", Issue.Status.WONTFIX, Severity.CRITICAL, Effort.HIGH),
        ("B", "not-found", Issue.Status.NOT_FOUND, Severity.ADVICE, Effort.LOW),
        ("B", "reopened", Issue.Status.REOPENED, Severity.UNDEFINED, Effort.HIGH),
        ("C", "is-found", Issue.Status.NEW, Severity.CRITICAL, Effort.HIGH),
        ("C", "not-found", Issue.Status.NOT_FOUND, Severity.WARNING, Effort.LOW),
    ]:
        kind = Kind(
            category="tests",
            namespace=namespace,
            id=id,
            severity=severity,
            effort=effort,
            title=f"Title for {namespace}:{id}",
            description=f"Description for {namespace}:{id} | Status: {{was}} -> {{is}}",
        )
        kinds[kind.key] = kind
        if namespace != "C":
            issue_factory(repository=repository, kind_key=kind.key, status=status.value)

    checks = [
        # known issues, found
        check_factory("A:new", True, {"was": "new", "is": "known"}),
        check_factory("A:fixed", True, {"was": "fixed", "is": "reopened"}),
        check_factory("A:wontfix", True, {"was": "wontfix", "is": "wontfix"}),
        check_factory("A:not-found", True, {"was": "not-found", "is": "new"}),
        check_factory("A:reopened", True, {"was": "reopened", "is": "known"}),
        # known issues, not found
        check_factory("B:new", False, {"was": "new", "is": "fixed"}),
        check_factory("B:fixed", False, {"was": "fixed", "is": "not-found"}),
        check_factory("B:wontfix", False, {"was": "wontfix", "is": "fixed"}),
        check_factory("B:not-found", False, {"was": "not-found", "is": "not-found"}),
        check_factory("B:reopened", False, {"was": "reopened", "is": "fixed"}),
        # new issues
        check_factory("C:is-found", True),
        check_factory("C:not-found", False),
    ]

    mocker.patch("zoo.api.mutations.CHECKS", checks)
    mocker.patch("zoo.auditing.check_discovery.KINDS", kinds)
    m_download_repository = mocker.patch(
        "zoo.api.mutations.download_repository", return_value=fake_path
    )

    yield repository, sha

    m_download_repository.assert_called_once_with(repository, mocker.ANY, sha=sha)


query = """
mutation test ($input: CheckRepositoryByCommitInput!) {
    checkRepositoryByCommit (input: $input) {
        allCheckResults {
            isFound
            kindKey
            status
            details
            severity
            effort
            title
            description
        }
    }
}
"""


def test_unknown_repository(snapshot, call_api):
    input = {"owner": "games", "name": "doom", "sha": "IDKFA"}
    response = call_api(query, input)

    snapshot.assert_match(response)


def test_all_results(scenario, snapshot, call_api):
    repository, sha = scenario

    input = {"owner": repository.owner, "name": repository.name, "sha": sha}
    response = call_api(query, input)

    snapshot.assert_match(response)


def test_only_found(scenario, snapshot, call_api):
    repository, sha = scenario

    input = {
        "owner": repository.owner,
        "name": repository.name,
        "sha": sha,
        "onlyFound": True,
    }
    response = call_api(query, input)

    snapshot.assert_match(response)


def test_with_repository(scenario, snapshot, call_api):
    repository, sha = scenario

    query = """
    mutation test ($input: CheckRepositoryByCommitInput!) {
        checkRepositoryByCommit (input: $input) {
            repository {
                id
                owner
                name
                url
                remoteId
            }
        }
    }
    """
    input = {"owner": repository.owner, "name": repository.name, "sha": sha}
    response = call_api(query, input)

    snapshot.assert_match(response)
