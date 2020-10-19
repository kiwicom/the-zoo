from django.urls import path

from . import views

urlpatterns = [path("search", views.MeiliSearchView.as_view(), name="search_overview")]
