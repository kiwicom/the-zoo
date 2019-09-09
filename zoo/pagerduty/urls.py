"""Pagerduty URL Configuration."""
from django.urls import path

from . import views

urlpatterns = [
    path(
        "services/<service_id>/",
        views.service_details,
        name="pagerduty_service_details",
    )
]
