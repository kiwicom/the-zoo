from django.contrib import admin

from . import models


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, *args, **kwargs):
        return not self.model.objects.exists()  # Allow only one entry on the database


class HelpersAdmin(SingletonAdmin):
    pass


class HintsAdmin(SingletonAdmin):
    pass


class PlaceholdersAdmin(SingletonAdmin):
    pass


admin.site.register(models.Helpers, HelpersAdmin)
admin.site.register(models.Hints, HintsAdmin)
admin.site.register(models.Placeholders, PlaceholdersAdmin)
