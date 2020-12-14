import json

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_open_bulk_git_issues__no_issues(mocker, client, user):
    m_task = mocker.patch("zoo.auditing.tasks.bulk_create_git_issues")

    client.force_login(user)
    body = json.dumps({"selectedIssues": {}, "filters": {"applied": []}})
    response = client.post(
        reverse("bulk_create_issues"), body, content_type="application/json"
    )

    assert response.status_code == 200
    m_task.delay.assert_called_once_with([])


def test_open_bulk_git_issues__has_issues(mocker, client, user, issue_factory):
    m_task = mocker.patch("zoo.auditing.tasks.bulk_create_git_issues")

    issue_1, issue_2 = issue_factory(), issue_factory()

    client.force_login(user)
    body = json.dumps(
        {
            "selectedIssues": {
                issue_1.kind_key: [issue_1.repository_id],
                issue_2.kind_key: [issue_2.repository_id],
            },
            "filters": {"applied": []},
        }
    )
    response = client.post(
        reverse("bulk_create_issues"), body, content_type="application/json"
    )

    assert response.status_code == 200
    m_task.delay.assert_called_once_with(
        [
            (issue_1.id, user.username, "http://testserver/auditing/"),
            (issue_2.id, user.username, "http://testserver/auditing/"),
        ]
    )


def test_open_bulk_git_issues__has_issues__with_owner(mocker, client, user, issue):
    m_task = mocker.patch("zoo.auditing.tasks.bulk_create_git_issues")

    client.force_login(user)
    body = json.dumps(
        {
            "selectedIssues": {issue.kind_key: [issue.repository_id]},
            "owner": "Simone",
            "filters": {"applied": []},
        }
    )
    response = client.post(
        reverse("bulk_create_issues"), body, content_type="application/json"
    )

    assert response.status_code == 200
    m_task.delay.assert_called_once_with(
        [(issue.id, user.username, "http://testserver/auditing/Simone/")]
    )


def test_apply_bulk_patches__no_issues(mocker, client, user):
    m_task = mocker.patch("zoo.auditing.tasks.bulk_apply_patches")

    client.force_login(user)
    body = json.dumps({"selectedIssues": {}, "filters": {"applied": []}})
    response = client.post(
        reverse("bulk_apply_patches"), body, content_type="application/json"
    )

    assert response.status_code == 200
    m_task.delay.assert_called_once_with([])


def test_apply_bulk_patches__has_issues(mocker, client, user, issue_factory):
    m_task = mocker.patch("zoo.auditing.tasks.bulk_apply_patches")

    issue_1, issue_2 = issue_factory(), issue_factory()

    client.force_login(user)
    body = json.dumps(
        {
            "selectedIssues": {
                issue_1.kind_key: [issue_1.repository_id],
                issue_2.kind_key: [issue_2.repository_id],
            },
            "filters": {"applied": []},
        }
    )
    response = client.post(
        reverse("bulk_apply_patches"), body, content_type="application/json"
    )

    assert response.status_code == 200
    m_task.delay.assert_called_once_with([issue_1.id, issue_2.id])


def test_get_issue_patch(mocker, client, user, issue_factory):
    mocker.patch(
        "zoo.auditing.models.Issue.get_patches", mocker.Mock(return_value=([], None))
    )
    issue = issue_factory()
    params = {
        "project_type": issue.repository.project_type,
        "owner_slug": issue.repository.owner,
        "name_slug": issue.repository.name,
        "issue_pk": issue.pk,
    }
    client.force_login(user)
    response = client.get(reverse("patch_issue", kwargs=params))
    assert response.status_code == 200
    assert "No auto-generated patches can be applied." in str(response.content)


def test_post_issue_patch(mocker, client, user, issue_factory):
    mocker.patch(
        "zoo.auditing.models.Issue.get_patches", mocker.Mock(return_value=([], None))
    )
    mocker.patch(
        "zoo.auditing.models.Issue.handle_patches", mocker.Mock(return_value=True)
    )
    issue = issue_factory()
    params = {
        "project_type": issue.repository.project_type,
        "owner_slug": issue.repository.owner,
        "name_slug": issue.repository.name,
    }
    client.force_login(user)
    response = client.post(
        reverse("patch_issue", kwargs={"issue_pk": issue.pk, **params}),
        content_type="application/json",
        follow=True,
    )
    assert response.redirect_chain == [(reverse("audit_report", kwargs=params), 302)]
