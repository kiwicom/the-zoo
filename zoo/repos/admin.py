from django.contrib import admin

from . import models


class RepoAdmin(admin.ModelAdmin):
    search_fields = ("remote_id", "owner", "name", "provider")


admin.site.register(models.Repository, RepoAdmin)
