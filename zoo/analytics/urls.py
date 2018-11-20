from django.urls import path

from . import views

urlpatterns = [
    path("analytics", views.AnalyticsOverview.as_view(), name="analytics_overview")
]
