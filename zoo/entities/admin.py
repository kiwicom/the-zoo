from django.contrib import admin

from . import models


@admin.register(models.Entity)
class EntityAdmin(admin.ModelAdmin):
    search_fields = ("name", "owner", "kind", "type")


@admin.register(models.Link)
class LinkAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ("product_owner", "project_owner")
