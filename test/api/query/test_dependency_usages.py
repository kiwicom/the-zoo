import pytest

from .test_dependencies import generate_dependency_usages

pytestmark = pytest.mark.django_db


def test_empty(snapshot, call_api):
    query = """
    query {
      allDependencyUsages{
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


def test_all(snapshot, call_api, generate_dependency_usages):
    query = """
    query {
      allDependencyUsages {
        totalCount
        edges {
          node {
            id
            majorVersion
            minorVersion
            version
            patchVersion
            forProduction
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


def test_first(snapshot, call_api, generate_dependency_usages):
    query = """
    query {
      allDependencyUsages (first: 2){
        totalCount
        edges {
          node {
            id
            majorVersion
            minorVersion
            version
            patchVersion
            forProduction
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


def test_first_after(snapshot, call_api, generate_dependency_usages):
    query = """
    query {
      allDependencyUsages (first: 2, after: "Mq=="){
        totalCount
        edges {
          node {
            id
            majorVersion
            minorVersion
            version
            patchVersion
            forProduction
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


def test_last(snapshot, call_api, generate_dependency_usages):
    query = """
    query {
      allDependencyUsages(last: 3){
        totalCount
        edges {
          node {
            id
            majorVersion
            minorVersion
            version
            patchVersion
            forProduction
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


def test_last_before(snapshot, call_api, generate_dependency_usages):
    query = """
    query {
      allDependencyUsages(last: 1, before: "Mgo="){
        totalCount
        edges {
          node {
            id
            majorVersion
            minorVersion
            version
            patchVersion
            forProduction
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


def test_with_dependency(snapshot, call_api, generate_dependency_usages):
    query = """
    query {
      allDependencyUsages{
        totalCount
        edges {
          node {
            id
            majorVersion
            minorVersion
            version
            patchVersion
            forProduction
            dependency {
                id
                name
                type
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


def test_with_repository(snapshot, call_api, generate_dependency_usages):
    query = """
    query {
      allDependencyUsages{
        totalCount
        edges {
          node {
            id
            majorVersion
            minorVersion
            version
            patchVersion
            forProduction
            repository {
                id
                remoteId
                owner
                name
                url
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
