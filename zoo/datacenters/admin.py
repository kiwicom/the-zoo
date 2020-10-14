from django.contrib import admin

from . import models


@admin.register(models.Datacenter)
class DatacenterAdmin(admin.ModelAdmin):
    search_fields = ("provider", "region")
