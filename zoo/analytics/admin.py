from django.contrib import admin

from . import models


class DependencyAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("type",)


class DependencyUsageAdmin(admin.ModelAdmin):
    search_fields = ("dependency__name", "repo__name")
    list_filter = ("repo", "dependency__type", "for_production")


admin.site.register(models.Dependency, DependencyAdmin)
admin.site.register(models.DependencyUsage, DependencyUsageAdmin)
