"""repos URL Configuration."""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.RepoList.as_view(), name="repo_list"),
    path("<provider>/<int:repo_id>/", views.repo_details, name="repo_details"),
    path("api/get-gitlab-envs/", views.get_gitlab_envs, name="get_gitlab_envs"),
]
