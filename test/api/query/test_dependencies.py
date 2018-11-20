import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def generate_dependency_usages(dependency_usage_factory):
    dependency_usage_factory(
        id=1,
        dependency__id=34,
        dependency__name="graphql",
        dependency__type="Python Library",
        major_version=3,
        minor_version=4,
        patch_version=6,
        version="3.4.6",
        for_production="t",
        repo__id=1339,
        repo__remote_id=2434,
        repo__name="lowe",
        repo__owner="dadivgross",
        repo__url="https://gitlab.com/davidgross/lowe",
    )
    dependency_usage_factory(
        id=2,
        dependency__id=30,
        dependency__name="html",
        dependency__type="Language",
        major_version=3,
        minor_version=4,
        patch_version=6,
        version="3.4.6",
        for_production="f",
        repo__id=14324,
        repo__remote_id=434,
        repo__name="john",
        repo__owner="malkovic",
        repo__url="https://gitlab.com/malkovic/john",
    )
    dependency_usage_factory(
        id=3,
        dependency__id=29,
        dependency__name="vue",
        dependency__type="Language",
        major_version=3,
        minor_version=5,
        patch_version=1,
        version="3.5.1",
        for_production="f",
        repo__id=13,
        repo__remote_id=9949,
        repo__name="xscott",
        repo__owner="brownkendra",
        repo__url="https://gitlab.com/brownkendra/xscott",
    )
    dependency_usage_factory(
        id=4,
        dependency__id=28,
        dependency__name="arrow",
        dependency__type="Python Library",
        major_version=2,
        minor_version=5,
        patch_version=1,
        version="2.5.1",
        for_production="f",
        repo__id=18,
        repo__remote_id=3599,
        repo__name="cole",
        repo__owner="ismith",
        repo__url="https://gitlab.com/ismith/cole",
    )
    dependency_usage_factory(
        id=5,
        dependency__id=31,
        dependency__name="graphql",
        dependency__type="Javascript Library",
        major_version=1,
        minor_version=2,
        patch_version=2,
        version="1.2.2",
        for_production="t",
        repo__id=33248,
        repo__remote_id=39823,
        repo__name="rachel39",
        repo__owner="martinez",
        repo__url="https://gitlab.com/martinez/rachel39",
    )


def test_empty(snapshot, call_api):
    query = """
    query {
      allDependencies{
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
      allDependencies {
        totalCount
        edges {
          node {
            id
            name
            type
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
      allDependencies (first: 2){
        totalCount
        edges {
          node {
            id
            name
            type
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
      allDependencies (first: 2, after: "Mq=="){
        totalCount
        edges {
          node {
            id
            name
            type
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
      allDependencies(last: 3){
        totalCount
        edges {
          node {
            id
            name
            type
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
      allDependencies(last: 1, before: "Mgo="){
        totalCount
        edges {
          node {
            id
            name
            type
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
      allDependencies{
        totalCount
        edges {
          node {
            id
            name
            type
            allDependencyUsages {
              edges {
                node {
                  id
                  majorVersion
                  patchVersion
                  forProduction
                  minorVersion
                  version
                }
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


def test_filter_by_name(snapshot, call_api, generate_dependency_usages):
    query = """
    query {
      allDependencies(name: "Graph") {
        totalCount
        edges {
          node {
            id
            name
            type
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


def test_filter_by_type(snapshot, call_api, generate_dependency_usages):
    query = """
    query {
      allDependencies(dependencyType: PY_LIB) {
        totalCount
        edges {
          node {
            id
            name
            type
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


def test_filter_by_type_and_name(snapshot, call_api, generate_dependency_usages):
    query = """
    query {
      allDependencies(dependencyType: PY_LIB, name:"Graph") {
        totalCount
        edges {
          node {
            id
            name
            type
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
