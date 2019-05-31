import pytest

from zoo.services.models import Service
from zoo.repos.models import Repository

pytestmark = pytest.mark.django_db


@pytest.fixture
def generate_services(service_factory):
    service_factory(
        id=1,
        name="martinez",
        owner="michaelbennett",
        impact="profit",
        dashboard_url="https://dashboard",
        docs_url="https://docsurl",
        pagerduty_url="https://pagerduty",
        slack_channel="https://slackchannel",
        status="fixed",
        health_check_url="https://healtcheck",
        repository__id=78,
        repository__remote_id=239,
        repository__owner="jasckson",
        repository__name="thiwer",
        repository__url="https://gitlab.com/thiwer/thiwer",
    )
    service_factory(
        id=2,
        name="alex",
        owner="amstrong",
        impact="profit",
        dashboard_url="https://dashboard",
        docs_url="https://docsurl",
        pagerduty_url="https://pagerduty",
        slack_channel="https://slackchannel",
        status="fixed",
        health_check_url="https://healtcheck",
        repository__id=48,
        repository__remote_id=99,
        repository__owner="colisn",
        repository__name="farel",
        repository__url="https://gitlab.com/farel/colins",
    )
    service_factory(
        id=3,
        name="artinez",
        owner="bennett",
        impact="profit",
        dashboard_url="https://dashboard",
        docs_url="https://docsurl",
        pagerduty_url="https://pagerduty",
        slack_channel="https://slackchannel",
        status="fixed",
        health_check_url="https://healtcheck",
        repository__id=234,
        repository__remote_id=9234,
        repository__owner="Daniel",
        repository__name="Amstrong",
        repository__url="https://gitlab.com/daniel/amstrong",
    )
    service_factory(
        id=4,
        name="john",
        owner="benneto",
        impact="profit",
        dashboard_url="https://dashboard",
        docs_url="https://docsurl",
        pagerduty_url="https://pagerduty",
        slack_channel="https://slackchannel",
        status="fixed",
        health_check_url="https://healtcheck",
        repository__id=3434,
        repository__remote_id=349,
        repository__owner="josh",
        repository__name="blanc",
        repository__url="https://gitlab.com/josh/blanc",
    )

    service_factory(
        id=12,
        name="simmons-mitchell",
        owner="dedward",
        impact="profit",
        dashboard_url="https://dashboard",
        docs_url="https://docsurl",
        pagerduty_url="https://pagerduty",
        slack_channel="https://slackchannel",
        status="fixed",
        health_check_url="https://healtcheck",
        repository__id=4543,
        repository__remote_id=990,
        repository__owner="imosley",
        repository__name="leblanc",
        repository__url="https://gitlab.com/schultzcarolyn/leblanc",
    )


def test_empty(snapshot, call_api):
    query = """
    query {
      allServices {
        totalCount
        edges {
          node {
            id
          }
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_all(snapshot, call_api, generate_services):
    query = """
    query {
      allServices {
        totalCount
        edges {
          node {
            id
            owner
            name
            status
            impact
            slackChannel
            pagerdutyUrl
            dashboardUrl
            docsUrl
            healthCheckUrl
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


def test_with_repository(snapshot, call_api, generate_services):
    query = """
    query{
      allServices {
        totalCount
        edges {
          node {
            id
            name
            owner
            status
            impact
            slackChannel
            pagerdutyUrl
            dashboardUrl
            docsUrl
            healthCheckUrl
            repository {
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


def test_first(snapshot, call_api, generate_services):
    query = """
    query {
      allServices(first: 3) {
        totalCount
        edges {
          node {
            id
            owner
            status
            impact
            slackChannel
            pagerdutyUrl
            dashboardUrl
            docsUrl
            healthCheckUrl
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


def test_first_after(snapshot, call_api, generate_services):
    query = """
    query {
      allServices(first: 2, after: "MQ==") {
        totalCount
        edges {
          node {
            id
            owner
            status
            impact
            slackChannel
            pagerdutyUrl
            dashboardUrl
            docsUrl
            healthCheckUrl
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


def test_last(snapshot, call_api, generate_services):
    query = """
    query {
      allServices(last: 3) {
        totalCount
        edges {
          node {
            id
            owner
            status
            impact
            slackChannel
            pagerdutyUrl
            dashboardUrl
            docsUrl
            healthCheckUrl
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


def test_last_before(snapshot, call_api, generate_services):
    query = """
    query {
      allServices(last: 1, before: "MQ==") {
        totalCount
        edges {
          node {
            id
            owner
            status
            impact
            slackChannel
            pagerdutyUrl
            dashboardUrl
            docsUrl
            healthCheckUrl
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
