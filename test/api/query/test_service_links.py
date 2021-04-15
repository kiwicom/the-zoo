import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def generate_links(service_factory, link_factory):
    service = service_factory(
        id=1,
        name="martinez",
        owner="michaelbennett",
        impact="profit",
        docs_url="https://docsurl",
        pagerduty_service="sales/P019873X9",
        slack_channel="https://slackchannel",
        status="fixed",
    )
    link_factory(
        id=1,
        service=service,
        name="Datadog",
        url="https://datadog.com",
        icon="datadog",
    )
    link_factory(
        id=2, service=service, name="Sentry", url="https://sentry.com", icon="sentry"
    )


def test_empty(snapshot, call_api):
    query = """
    query {
      allServices {
        totalCount
        edges {
          node {
            allLinks {
              totalCount
              edges {
                node {
                  id
                }
              }
            }
          }
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_all(snapshot, call_api, generate_links):
    query = """
    query {
      allServices {
        totalCount
        edges {
          node {
            allLinks {
              totalCount
              edges {
                node {
                  id
                  name
                  url
                  icon
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
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_first(snapshot, call_api, generate_links):
    query = """
    query {
      allServices {
        totalCount
        edges {
          node {
            allLinks(first: 2) {
              totalCount
              edges {
                node {
                  id
                  name
                  url
                  icon
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
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_last(snapshot, call_api, generate_links):
    query = """
    query {
      allServices {
        totalCount
        edges {
          node {
            allEnvironments(last: 2, before: "Mg==") {
              totalCount
              edges {
                node {
                  id
                  name
                  url
                  icon
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
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)
