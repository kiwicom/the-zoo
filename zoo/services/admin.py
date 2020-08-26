from django.contrib import admin

from . import models


class ServiceAdmin(admin.ModelAdmin):
    search_fields = (
        "owner",
        "name",
        "repository__owner",
        "repository__name",
        "repository__remote_id",
    )


class EnvironmentAdmin(admin.ModelAdmin):
    search_fields = ("name", "service_urls", "dashboard_url")


class TierAdmin(admin.ModelAdmin):
    list_display = ("__str__", "description")


admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Environment, EnvironmentAdmin)
admin.site.register(models.Tier, TierAdmin)
