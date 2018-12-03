"""services URL Configuration."""
from django.urls import include, path

from . import views

global_urls = [path("", views.GlobalChecklistsView.as_view(), name="global_checklists")]

service_urls = [
    path("", views.ServiceChecklistView.as_view(), name="service_checklist"),
    path(
        "<str:checklist_item_key>/",
        views.update_service_checklist,
        name="service_checklist_update",
    ),
]

urlpatterns = [
    path("checklists/", include(global_urls)),
    path(
        "services/<str:service_owner_slug>/<str:service_name_slug>/checklist/",
        include(service_urls),
    ),
]
