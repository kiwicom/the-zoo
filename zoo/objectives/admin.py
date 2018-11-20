from django.contrib import admin

from . import models


class ObjectiveAdmin(admin.ModelAdmin):
    search_fields = ("service__owner", "service__name")


class ObjectiveSnapshotAdmin(admin.ModelAdmin):
    search_fields = ("objective__service__owner", "objective__service__name")


admin.site.register(models.Objective, ObjectiveAdmin)
admin.site.register(models.ObjectiveSnapshot, ObjectiveSnapshotAdmin)
