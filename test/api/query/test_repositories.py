import pytest

from zoo.repos import models
from zoo.repos.models import Repository

from .test_dependency_usages import generate_dependency_usages
from .test_issues import generate_issues

pytestmark = pytest.mark.django_db


@pytest.fixture
def generate_repositories(repository_factory):
    repository_factory(
        id=1,
        remote_id=11,
        name="marshall-evans",
        owner="pmiranda",
        url="https://gitlab.com/pmiranda/marshall-evans",
    )
    repository_factory(
        id=2,
        remote_id=12,
        name="evans",
        owner="orange",
        url="https://gitlab.com/orange/evans",
    )
    repository_factory(
        id=3,
        remote_id=33,
        name="serr",
        owner="olivia",
        url="https://gitlab.com/olivia/serr",
    )
    repository_factory(
        id=4,
        remote_id=21,
        name="serrano",
        owner="osbornolivia",
        url="https://gitlab.com/osbornolivia/serrano",
    )
    repository_factory(
        id=5,
        remote_id=22,
        name="malboro",
        owner="tag",
        url="https://gitlab.com/tag/malboro",
    )


def test_empty(snapshot, call_api):
    query = """
    query {
      allRepositories {
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


def test_all(snapshot, call_api, generate_repositories):
    query = """
    query {
      allRepositories {
        totalCount
        edges {
          node {
            id
            owner
            name
            url
            remoteId
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


def test_with_issue(snapshot, call_api, generate_issues):
    query = """
    query {
      allRepositories {
        totalCount
        edges {
          node {
            id
            owner
            name
            url
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


def test_first(snapshot, call_api, generate_repositories):
    query = """
    query {
      allRepositories(first: 3){
        totalCount
        edges {
          node {
            id
            owner
            name
            url
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


def test_first_after(snapshot, call_api, generate_repositories):
    query = """
    query {
      allRepositories(first: 2, after: "MQ=="){
        totalCount
        edges {
          node {
            id
            owner
            name
            url
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


def test_last(snapshot, call_api, generate_repositories):
    query = """
    query {
      allRepositories(last: 3){
        totalCount
        edges {
          node {
            id
            owner
            name
            url
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


def test_last_before(snapshot, call_api, generate_repositories):
    query = """
    query {
      allRepositories(last: 1, before: "Mgo="){
        totalCount
        edges {
          node {
            id
            owner
            name
            url
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


def test_with_dependency_usage(snapshot, call_api, generate_dependency_usages):
    query = """
    query {
      allRepositories {
        totalCount
        edges {
          node {
            id
            owner
            name
            url
            allDependencyUsages {
              totalCount
              edges {
                node {
                  id
                  majorVersion
                  minorVersion
                  patchVersion
                  forProduction
                  version
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
