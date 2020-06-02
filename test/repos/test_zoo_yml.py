import pytest
import yaml

from zoo.repos import zoo_yml as uut
from zoo.repos.models import Repository
from zoo.services.models import Environment, Service

pytestmark = pytest.mark.django_db


@pytest.fixture()
def service_1(db) -> Service:
    repo = Repository.objects.create(
        remote_id=11,
        name="test_proj1",
        owner="john_doe1",
        url="https://github.com/john_doe1/test_proj1",
        provider="github",
    )
    service = Service.objects.create(
        owner="test_owner",
        name="test_service",
        status="beta",
        impact="profit",
        slack_channel="https://test_service/slack",
        sentry_project="https://test_service/sentry",
        sonarqube_project="https://test_service/sonarqube",
        pagerduty_url="https://test_service/pager_duty",
        docs_url="https://test_service/docs",
        tags=["test"],
        repository=repo,
    )

    env = Environment.objects.create(
        service=service,
        name="production",
        service_urls=["https://test_service/production"],
        health_check_url="https://test_service/health",
        dashboard_url="https://test_service/dashboard",
        logs_url="https://test_service/logs",
    )

    service.environments.add(env)

    return service


def test_generate(service_1):
    content = uut.generate(service_1)
    assert uut.validate(content)
