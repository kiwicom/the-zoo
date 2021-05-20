from django.urls import path

from . import views

urlpatterns = [path("search", views.GlobalSearchView.as_view(), name="search_overview")]
