from django.contrib import admin

from . import models


@admin.register(models.Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    search_fields = ("service__owner", "service__name")


@admin.register(models.ObjectiveSnapshot)
class ObjectiveSnapshotAdmin(admin.ModelAdmin):
    search_fields = ("objective__service__owner", "objective__service__name")
