from django.forms import widgets

from .models import Repository


class RepoInput(widgets.TextInput):
    template_name = "repos/fields/repo_input.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs["list"] = "repos"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["repos"] = (
            Repository.objects.order_by("owner", "name")
            .only("pk", "owner", "name", "provider")
            .all()
        )

        context["widget"]["value"] = value
        return context
