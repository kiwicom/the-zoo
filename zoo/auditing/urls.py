"""services URL Configuration."""
from django.urls import include, path

from . import views

global_urls = [
    path("", views.AuditOverview.as_view(), name="audit_overview"),
    path("bulk_create/", views.open_bulk_git_issues, name="bulk_create_issues"),
    path("bulk_apply/", views.apply_bulk_patches, name="bulk_apply_patches"),
    path(
        "<str:owner_slug>/", views.AuditOverview.as_view(), name="owned_audit_overview"
    ),
]

project_urls = [
    path("", views.AuditReport.as_view(), name="audit_report"),
    path("<int:issue_pk>/gitlab_issue", views.open_git_issue, name="open_git_issue"),
    path("<int:issue_pk>/wontfix", views.wontfix_issue, name="wontfix_issue"),
    path("<int:issue_pk>/patch", views.IssuePatch.as_view(), name="patch_issue"),
]

urlpatterns = [
    path("auditing/", include(global_urls)),
    path(
        "<str:project_type>/<str:owner_slug>/<str:name_slug>/auditing/",
        include(project_urls),
    ),
]
