import pytest
import yaml

from zoo.repos import zoo_yml as uut
from zoo.repos.models import Repository
from zoo.services.models import Environment, Service

pytestmark = pytest.mark.django_db


@pytest.fixture
def generate_services_with_environments_and_links(
    service_factory, environment_factory, link_factory
):
    service = service_factory(
        id=1,
        name="martinez",
        owner="michaelbennett",
        impact="profit",
        docs_url="https://docsurl",
        pagerduty_service="/services",
        slack_channel="https://slackchannel",
        status="beta",
        repository__id=78,
        repository__remote_id=239,
        repository__owner="jasckson",
        repository__name="thiwer",
        repository__url="https://gitlab.com/thiwer/thiwer",
    )
    environment_factory(
        id=1,
        service=service,
        name="production",
        service_urls=["https://serviceurl1", "https://serviceurl2"],
        dashboard_url="https://dashboardurl",
        health_check_url="https://healthcheckurl",
    )
    environment_factory(
        id=2,
        service=service,
        name="staging",
        service_urls=["https://serviceurl1", "https://serviceurl2"],
        dashboard_url="https://dashboardurl",
    )
    link_factory(
        id=1,
        name="Datadog",
        url="https://dashboard.datadog.com",
        icon="poop",
        service=service,
    )
    link_factory(
        id=2, name="Sentry", url="https://dashboard.sentry.com", service=service
    )


def test_generate(generate_services_with_environments_and_links):
    expected = """
type: service
name: martinez
owner: michaelbennett
impact: profit
status: beta
docs_url: https://docsurl
slack_channel: https://slackchannel
sentry_project: null
sonarqube_project: null
pagerduty_service: /services
tags: []
environments:
- name: production
  dashboard_url: https://dashboardurl
  health_check_url: https://healthcheckurl
  service_urls:
  - https://serviceurl1
  - https://serviceurl2
- name: staging
  dashboard_url: https://dashboardurl
  health_check_url: null
  service_urls:
  - https://serviceurl1
  - https://serviceurl2
links:
- name: Datadog
  url: https://dashboard.datadog.com
  icon: poop
- name: Sentry
  url: https://dashboard.sentry.com
  icon: null
"""
    service_1 = Service.objects.get(pk=1)
    content = uut.generate(service_1)
    assert uut.validate(content)
    assert expected.strip() == content.strip()
