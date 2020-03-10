import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_library_overview(client, user):
    client.force_login(user)
    response = client.get(reverse("library_overview"))
    assert response.status_code == 200


def test_dependency_overview(client, user):
    client.force_login(user)
    response = client.get(reverse("dependency_overview"))
    assert response.status_code == 200


def test_ci_template_overview(client, user):
    client.force_login(user)
    response = client.get(reverse("ci_template_overview"))
    assert response.status_code == 200


def test_project_template_overview(client, user):
    client.force_login(user)
    response = client.get(reverse("project_template_overview"))
    assert response.status_code == 200


def test_language_overview(client, user):
    client.force_login(user)
    response = client.get(reverse("language_overview"))
    assert response.status_code == 200
