from django.contrib import admin

from . import models


@admin.register(models.Library)
class LibraryAdmin(admin.ModelAdmin):
    search_fields = (
        "owner",
        "name",
        "repository__owner",
        "repository__name",
        "repository__remote_id",
    )
