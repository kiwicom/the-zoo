from django.contrib import admin

from . import models


class DatacenterAdmin(admin.ModelAdmin):
    search_fields = ("provider", "region")


admin.site.register(models.Datacenter, DatacenterAdmin)
