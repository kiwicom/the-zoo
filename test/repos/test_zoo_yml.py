import pytest
import yaml

from zoo.repos import zoo_yml as uut
from zoo.repos.models import Repository
from zoo.services.models import Environment, Service

pytestmark = pytest.mark.django_db


@pytest.fixture
def generate_services_with_environments(service_factory, environment_factory):
    service = service_factory(
        id=1,
        name="martinez",
        owner="michaelbennett",
        impact="profit",
        docs_url="https://docsurl",
        pagerduty_url="https://pagerduty",
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
        health_check_url="https://healthcheckurl",
    )


def test_generate(generate_services_with_environments):
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
pagerduty_url: https://pagerduty
tags:
- general
environments:
- name: staging
  dashboard_url: https://dashboardurl
  health_check_url: https://healthcheckurl
  service_urls:
  - https://serviceurl1
  - https://serviceurl2
- name: production
  dashboard_url: https://dashboardurl
  health_check_url: https://healthcheckurl
  service_urls:
  - https://serviceurl1
  - https://serviceurl2

"""
    service_1 = Service.objects.get(pk=1)
    content = uut.generate(service_1)
    assert uut.validate(content)
    assert expected.strip() == content.strip()
