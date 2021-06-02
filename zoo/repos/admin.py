from django.contrib import admin

from . import models


@admin.register(models.Repository)
class RepoAdmin(admin.ModelAdmin):
    search_fields = ("remote_id", "owner", "name", "provider")


@admin.register(models.RepositoryEnvironment)
class RepoEnvAdmin(admin.ModelAdmin):
    search_fields = ("name", "external_url")
