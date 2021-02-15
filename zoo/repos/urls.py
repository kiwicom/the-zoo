"""repos URL Configuration."""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.RepoList.as_view(), name="repo_list"),
]
