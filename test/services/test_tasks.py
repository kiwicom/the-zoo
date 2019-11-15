import json

import faker
import httpretty
import pytest

from zoo.services import models
from zoo.services import tasks as uut

fake = faker.Faker()


@httpretty.activate
def test_fetch_sonarqube_projects(mocker):
    sonarqube_url = "https://tests.kiwi.com"
    mocker.patch("zoo.services.tasks.settings.SONARQUBE_URL", sonarqube_url)

    data_p1 = {
        "paging": {"pageIndex": 1, "pageSize": 2, "total": 3},
        "components": [
            {
                "organization": "default-organization",
                "id": fake.pystr(),
                "key": "aaa:bbb",
                "name": "aaa:bbb",
                "qualifier": "TRK",
                "visibility": "public",
                "lastAnalysisDate": "2018-12-28T20:14:21+0000",
            },
            {
                "organization": "default-organization",
                "id": fake.pystr(),
                "key": "bbb:ccc",
                "name": "bbb:ccc",
                "qualifier": "TRK",
                "visibility": "public",
                "lastAnalysisDate": "2019-01-14T16:17:21+0000",
            },
        ],
    }
    data_p2 = {
        "paging": {"pageIndex": 2, "pageSize": 2, "total": 3},
        "components": [
            {
                "organization": "default-organization",
                "id": fake.pystr(),
                "key": "ccc:ddd",
                "name": "ccc:ddd",
                "qualifier": "TRK",
                "visibility": "public",
                "lastAnalysisDate": "2019-01-14T16:17:21+0000",
            }
        ],
    }

    httpretty.register_uri(
        httpretty.GET,
        f"{sonarqube_url}/api/projects/search?p=1",
        body=json.dumps(data_p1),
        match_querystring=True,
    )
    httpretty.register_uri(
        httpretty.GET,
        f"{sonarqube_url}/api/projects/search?p=2",
        body=json.dumps(data_p2),
        match_querystring=True,
    )

    projects = uut.fetch_sonarqube_projects()

    expected_result = data_p1["components"]
    expected_result.extend(data_p2["components"])
    assert projects == expected_result


@httpretty.activate
def test_fetch_sonarqube_project_links(mocker):
    sonarqube_url = "https://tests.kiwi.com"
    mocker.patch("zoo.services.tasks.settings.SONARQUBE_URL", sonarqube_url)

    data = {
        "links": [
            {
                "id": fake.pystr(),
                "type": "homepage",
                "url": "https://gitlab.example.com/test/backend",
            },
            {
                "id": fake.pystr(),
                "type": "ci",
                "url": "https://gitlab.example.com/test/backend/pipelines",
            },
        ]
    }
    project_key = "test:backend"

    httpretty.register_uri(
        httpretty.GET,
        f"{sonarqube_url}/api/project_links/search?projectKey={project_key}",
        body=json.dumps(data),
        match_querystring=True,
    )

    links = uut.fetch_sonarqube_project_links(project_key)
    assert links == data["links"]


@pytest.mark.django_db
def test_sync_sonarqube_projects(mocker, service_factory, repository_factory):
    mocker.patch(
        "zoo.services.tasks.fetch_sonarqube_projects",
        return_value=[
            {
                "organization": "default-organization",
                "id": fake.pystr(),
                "key": "aaa:bbb",
                "name": "aaa:bbb",
                "qualifier": "TRK",
                "visibility": "public",
                "lastAnalysisDate": "2018-12-28T20:14:21+0000",
            }
        ],
    )
    mocker.patch(
        "zoo.services.tasks.fetch_sonarqube_project_links",
        return_value=[
            {
                "id": fake.pystr(),
                "type": "homepage",
                "url": "https://gitlab.example.com/test/backend",
            }
        ],
    )

    repository = repository_factory(url="https://gitlab.example.com/test/backend")
    service = service_factory(repository=repository)
    service_without_repo = service_factory(repository=None)

    repository.save()
    service.save()
    service_without_repo.save()

    uut.sync_sonarqube_projects()

    service = models.Service.objects.get(sonarqube_project="aaa:bbb")
    assert service is not None
