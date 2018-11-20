from django.contrib import admin

from . import models


class IssueAdmin(admin.ModelAdmin):
    search_fields = ("kind_key",)


admin.site.register(models.Issue, IssueAdmin)
