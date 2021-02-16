from base64 import b64encode

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
      repositories {
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
      repositories {
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
      repositories {
        edges {
          node {
            id
            owner
            name
            url
            issues {
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
      repositories(first: 3){
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
      repositories(first: 2, after: "MQ=="){
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
      repositories(last: 3){
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
      repositories(last: 1, before: "Mgo="){
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
      repositories {
        edges {
          node {
            id
            owner
            name
            url
            dependencyUsages {
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


def test_with_project_details(snapshot, call_api, mocker, repository_factory):
    repository_factory(id=1)
    query = """
    query ($id: ID!) {
        repository(id: $id) {
            projectDetails {
                id
                name
                description
                avatar
                url
                readme
                stars
                forks
                branchCount
                memberCount
                issueCount
                lastActivityAt
            }
        }
    }
    """
    mocker.patch(
        "zoo.repos.models.Repository.project_details",
        repository_factory._project_details,
    )
    response = call_api(query, id=str(b64encode(b"Repository:1")))
    snapshot.assert_match(response)
