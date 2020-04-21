from django.urls import path

from . import search

urlpatterns = [
    path("search", search.ElasticSearchView.as_view(), name="search_overview")
]
