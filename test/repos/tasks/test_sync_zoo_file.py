from typing import Dict, List, Union

import pytest

from zoo.repos import tasks as uut
from zoo.repos.models import Repository
from zoo.repos.zoo_yml import parse
from zoo.services.models import Environment, Service

pytestmark = pytest.mark.django_db


@pytest.fixture()
def generate_repositories(repository_factory):
    repository_factory(
        id=1,
        remote_id=11,
        name="test_proj1",
        owner="john_doe1",
        url="https://github.com/john_doe1/test_proj1",
        provider="github",
    )


def test_update_or_create_service(generate_repositories):
    data = {
        "type": "service",
        "name": "test_proj1",
        "owner": "john_doe1",
        "impact": "profit",
        "status": "beta",
        "docs_url": "http://test_proj1/docs",
        "slack_channel": "#test_proj1",
        "sentry_project": "http://test_proj1/sentry",
        "sonarqube_project": "http://test_proj1/sonarqube",
        "pagerduty_service": "/services",
        "tags": ["tag1", "tag2", "tag3"],
        "environments": [
            {
                "name": "staging",
                "dashboard_url": "http://staging.test_proj1/dashboard",
                "service_urls": [
                    "http://staging.test_proj1/service1",
                    "http://staging.test_proj1/service2",
                ],
                "health_check_url": "http://staging.test_proj1/health_check",
            },
            {
                "name": "production",
                "dashboard_url": "http://production.test_proj1/dashboard",
                "service_urls": [
                    "http://production.test_proj1/service1",
                    "http://production.test_proj1/service2",
                ],
                "health_check_url": "http://production.test_proj1/health_check",
            },
        ],
    }

    proj = {"id": 11, "provider": "github"}

    uut.update_or_create_service(data, proj)
    service = Service.objects.filter(owner=data["owner"], name=data["name"]).first()
    assert (
        service is not None
    ), f"Service with owner: {data['owner']} and name: {data['name']} not found"
    assert_service(service, data)

    envs = Environment.objects.filter(service=service)
    assert envs.count() == 2, f"Got {envs.count()} , want: 2 environments"

    for env in envs.all():
        expected = get_expected_env(env.name, data["environments"])
        assert expected is not None
        assert_environment(env, expected)


def test_update_project_from_zoo_file(mocker):
    zoo_yml = """
    type: service
    name: test_proj1
    owner: john_doe1
    impact: profit
    status: beta
    docs_url: http://test_proj1/docs
    slack_channel: "#test_proj1"
    sentry_project: http://test_proj1/sentry
    sonarqube_project: http://test_proj1/sonarqube
    pagerduty_service: /services
    tags:
        - tag1
        - tag2
        - tag3
    environments:
        -
            name: staging
            dashboard_url: http://staging.test_proj1/dashboard
            service_urls:
                - http://staging.test_proj1/service1
                - http://staging.test_proj1/service2
            health_check_url: http://staging.test_proj1/health_check
        -
            name: production
            dashboard_url: http://production.test_proj1/dashboard
            service_urls:
                - http://production.test_proj1/service1
                - http://production.test_proj1/service2
            health_check_url: http://production.test_proj1/health_check
    """
    data = parse(zoo_yml)

    m_get_zoo_file_content = mocker.patch(
        "zoo.repos.tasks.get_zoo_file_content", return_value=zoo_yml
    )
    m_update_or_create_service = mocker.patch(
        "zoo.repos.tasks.update_or_create_service", return_value=None
    )

    proj = {"id": 11, "provider": "github"}
    uut.update_project_from_zoo_file(proj)

    m_get_zoo_file_content.assert_called_once_with(proj)
    m_update_or_create_service.assert_called_once_with(data, proj)


def assert_service(got: Service, expected: Dict) -> None:
    assert got.owner == expected["owner"]
    assert got.name == expected["name"]
    assert got.impact == expected["impact"]
    assert got.status == expected["status"]
    assert got.docs_url == expected["docs_url"]
    assert got.slack_channel == expected["slack_channel"]
    assert got.sentry_project == expected["sentry_project"]
    assert got.sonarqube_project == expected["sonarqube_project"]
    assert got.pagerduty_service == expected["pagerduty_service"]
    assert_tags(got.tags, expected["tags"])


def assert_environment(got: Environment, expected: Dict) -> None:
    assert got.name == expected["name"]
    assert got.dashboard_url == expected["dashboard_url"]
    assert len(got.service_urls) == len(expected["service_urls"])
    assert got.health_check_url == expected["health_check_url"]


def assert_tags(got: List, expected: List):
    # because pre_save signal on Service
    if "general" not in expected:
        expected.append("general")

    assert len(got) == len(expected)
    assert sorted(got) == sorted(expected)


def get_expected_env(name: str, envs: List) -> Union[Dict, None]:
    for env in envs:
        if env["name"] == name:
            return env
    return None
