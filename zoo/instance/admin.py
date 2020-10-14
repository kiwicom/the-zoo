from django.contrib import admin

from . import models


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, *args, **kwargs):
        return not self.model.objects.exists()  # Allow only one entry on the database


@admin.register(models.Helpers)
class HelpersAdmin(SingletonAdmin):
    pass


@admin.register(models.Hints)
class HintsAdmin(SingletonAdmin):
    pass


@admin.register(models.Placeholders)
class PlaceholdersAdmin(SingletonAdmin):
    pass
