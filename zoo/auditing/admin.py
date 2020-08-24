from django.contrib import admin

from .models import Issue


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    search_fields = ("kind_key",)
