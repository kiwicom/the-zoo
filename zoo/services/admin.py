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


class DataCenterAdmin(admin.ModelAdmin):
    search_fields = ("provider", "region")


admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.DataCenter, DataCenterAdmin)
