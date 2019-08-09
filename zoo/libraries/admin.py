from django.contrib import admin

from . import models


class LibraryAdmin(admin.ModelAdmin):
    search_fields = (
        "owner",
        "name",
        "repository__owner",
        "repository__name",
        "repository__remote_id",
    )


admin.site.register(models.Library, LibraryAdmin)
