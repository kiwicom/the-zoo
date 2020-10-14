from django.contrib import admin

from . import models


@admin.register(models.Dependency)
class DependencyAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("type",)


@admin.register(models.DependencyUsage)
class DependencyUsageAdmin(admin.ModelAdmin):
    search_fields = ("dependency__name", "repo__name")
    list_filter = ("repo", "dependency__type", "for_production")
