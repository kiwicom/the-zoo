from django.contrib import admin

from . import models


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    search_fields = (
        "owner",
        "name",
        "repository__owner",
        "repository__name",
        "repository__remote_id",
    )


@admin.register(models.Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    search_fields = ("name", "service_urls", "dashboard_url")


@admin.register(models.Tier)
class TierAdmin(admin.ModelAdmin):
    list_display = ("__str__", "description")
