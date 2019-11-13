"""repos URL Configuration."""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.RepoList.as_view(), name="repo_list"),
    path("<provider>/<int:repo_id>/", views.repo_details, name="repo_details"),
    path(
        "<provider>/<int:repo_id>/openapi",
        views.openapi_definition,
        name="repo_openapi",
    ),
]
