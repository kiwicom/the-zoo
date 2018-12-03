from django.contrib import admin

from . import models


class CheckmarkAdmin(admin.ModelAdmin):
    search_fields = ("item_key",)


admin.site.register(models.Checkmark, CheckmarkAdmin)
