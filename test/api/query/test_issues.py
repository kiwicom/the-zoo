import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def generate_issues(issue_factory):
    issue_factory(
        id=1,
        last_check="2018-09-03 13:09:21.022164+00:00",
        details={"I": True, "data": "restored"},
        remote_issue_id=62,
        repository__id=36,
        repository__name="blumed",
        repository__owner="john",
        repository__url="https://home.com/url",
        repository__remote_id=234,
        comment="Saturn",
        kind_key="moran:alex",
    )
    issue_factory(
        id=2,
        last_check="2018-09-03 13:09:21.022164+00:00",
        details={"need": True, "data": "restored"},
        remote_issue_id=636,
        repository__id=37,
        repository__name="fisher",
        repository__owner="john",
        repository__url="https://home.com/url",
        repository__remote_id=754,
        comment="Juno",
        kind_key="cook:alice",
    )
    issue_factory(
        id=3,
        last_check="2018-09-03 13:09:21.022164+00:00",
        details={"more": True, "data": "restored"},
        remote_issue_id=6346,
        repository__id=38,
        repository__name="bomer",
        repository__owner="john",
        repository__url="https://home.com/url",
        repository__remote_id=987,
        comment="Jupiter",
        kind_key="pride-moran:john",
    )
    issue_factory(
        id=4,
        last_check="2018-09-03 13:09:21.022164+00:00",
        details={"power": True, "data": "restored"},
        remote_issue_id=9346,
        repository__id=39,
        repository__name="jackson",
        repository__owner="john",
        repository__url="https://home.com/url",
        repository__remote_id=246,
        comment="Herse",
        kind_key="denis:roman",
    )
    issue_factory(
        id=5,
        last_check="2018-09-03 13:09:21.022164+00:00",
        details={"now!": True, "data": "restored"},
        remote_issue_id=65,
        repository__id=40,
        repository__name="musher",
        repository__owner="john",
        repository__url="https://home.com/url",
        repository__remote_id=2334,
        comment="Pluto",
        kind_key="dennis:moran",
    )


def test_empty(snapshot, call_api):
    query = """
    query {
      allIssues{
        totalCount
        edges {
          node {
            id
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_all(snapshot, call_api, generate_issues):
    query = """
    query {
      allIssues {
        totalCount
        edges {
          node {
            id
            kindKey
            status
            details
            remoteIssueId
            comment
            lastCheck
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_first(snapshot, call_api, generate_issues):
    query = """
    query {
      allIssues (first: 2){
        totalCount
        edges {
          node {
            id
            kindKey
            status
            details
            remoteIssueId
            comment
            lastCheck
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_first_after(snapshot, call_api, generate_issues):
    query = """
    query {
      allIssues (first: 2, after: "MQ=="){
        totalCount
        edges {
          node {
            id
            kindKey
            status
            details
            remoteIssueId
            comment
            lastCheck
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_last(snapshot, call_api, generate_issues):
    query = """
    query {
      allIssues(last: 3){
        totalCount
        edges {
          node {
            id
            kindKey
            status
            details
            remoteIssueId
            comment
            lastCheck
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_last_before(snapshot, call_api, generate_issues):
    query = """
    query {
      allIssues(last: 1, before: "Mgo="){
        totalCount
        edges {
          node {
            id
            kindKey
            status
            details
            remoteIssueId
            comment
            lastCheck
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_with_repository(snapshot, call_api, generate_issues):
    query = """
    query {
      allIssues{
        totalCount
        edges {
          node {
            id
            repository {
              id
              name
              owner
              url
              remoteId
            }
            kindKey
            status
            details
            remoteIssueId
            comment
            lastCheck
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)
