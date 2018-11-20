"""services URL Configuration."""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.AuditOverview.as_view(), name="audit_overview"),
    path("bulk_create/", views.open_bulk_git_issues, name="bulk_create_issues"),
    path(
        "<str:service_owner_slug>/",
        views.AuditOverview.as_view(),
        name="owned_audit_overview",
    ),
    path(
        "<str:service_owner_slug>/<str:service_name_slug>",
        views.AuditReport.as_view(),
        name="audit_report",
    ),
    path(
        "<str:service_owner_slug>/<str:service_name_slug>/issues/<int:issue_pk>/gitlab_issue",
        views.open_git_issue,
        name="open_git_issue",
    ),
    path(
        "<str:service_owner_slug>/<str:service_name_slug>/issues/<int:issue_pk>/wontfix",
        views.wontfix_issue,
        name="wontfix_issue",
    ),
]
