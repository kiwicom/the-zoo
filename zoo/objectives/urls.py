"""services URL Configuration."""
from django.urls import path

from . import views

urlpatterns = [path("", views.ObjectiveList.as_view(), name="objective_list")]
