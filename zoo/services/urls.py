"""services URL Configuration."""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.ServiceList.as_view(), name="service_list"),
    path(
        "<str:owner_slug>/<str:name_slug>",
        views.ServiceDetail.as_view(),
        name="service_detail",
    ),
    path(
        "<str:owner_slug>/<str:name_slug>/openapi",
        views.ServiceOpenApiDefinition.as_view(),
        name="service_openapi",
    ),
    path(
        "<str:owner_slug>/<str:name_slug>/update",
        views.ServiceUpdate.as_view(),
        name="service_update",
    ),
    path(
        "<str:owner_slug>/<str:name_slug>/delete",
        views.ServiceDelete.as_view(),
        name="service_delete",
    ),
    path("new", views.ServiceCreate.as_view(), name="service_create"),
    path("new", views.ServiceCreate.as_view(), name="get_gitlab_envs"),
    path("api/get-gitlab-envs/", views.get_gitlab_envs, name="get_gitlab_envs"),
]
