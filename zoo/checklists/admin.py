from django.contrib import admin

from . import models


@admin.register(models.Checkmark)
class CheckmarkAdmin(admin.ModelAdmin):
    search_fields = ("item_key",)
