"""services URL Configuration."""
from django.urls import include, path

from . import views

global_urls = [
    path("", views.AuditOverview.as_view(), name="audit_overview"),
    path("bulk_create/", views.open_bulk_git_issues, name="bulk_create_issues"),
    path(
        "<str:service_owner_slug>/",
        views.AuditOverview.as_view(),
        name="owned_audit_overview",
    ),
]

service_urls = [
    path("", views.AuditReport.as_view(), name="audit_report"),
    path("<int:issue_pk>/gitlab_issue", views.open_git_issue, name="open_git_issue"),
    path("<int:issue_pk>/wontfix", views.wontfix_issue, name="wontfix_issue"),
]

urlpatterns = [
    path("auditing/", include(global_urls)),
    path(
        "services/<str:service_owner_slug>/<str:service_name_slug>/auditing/",
        include(service_urls),
    ),
]
