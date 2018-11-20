import json

from django.urls import reverse
import pytest

pytestmark = pytest.mark.django_db


def test_open_bulk_git_issues__no_issues(mocker, client, user):
    m_task = mocker.patch("zoo.auditing.tasks.bulk_create_git_issues")

    client.force_login(user)
    body = json.dumps({"pk_list": [], "filters": {"applied": []}})
    response = client.post(
        reverse("bulk_create_issues"), body, content_type="application/json"
    )

    assert response.status_code == 200
    m_task.delay.assert_called_once_with([])


def test_open_bulk_git_issues__has_issues(mocker, client, user):
    m_task = mocker.patch("zoo.auditing.tasks.bulk_create_git_issues")

    client.force_login(user)
    body = json.dumps({"pk_list": [13, 42], "filters": {"applied": []}})
    response = client.post(
        reverse("bulk_create_issues"), body, content_type="application/json"
    )

    assert response.status_code == 200
    m_task.delay.assert_called_once_with(
        [
            (13, user.username, "http://testserver/auditing/"),
            (42, user.username, "http://testserver/auditing/"),
        ]
    )


def test_open_bulk_git_issues__has_issues__with_owner(mocker, client, user):
    m_task = mocker.patch("zoo.auditing.tasks.bulk_create_git_issues")

    client.force_login(user)
    body = json.dumps({"pk_list": [666], "owner": "Simone", "filters": {"applied": []}})
    response = client.post(
        reverse("bulk_create_issues"), body, content_type="application/json"
    )

    assert response.status_code == 200
    m_task.delay.assert_called_once_with(
        [(666, user.username, "http://testserver/auditing/Simone/")]
    )
