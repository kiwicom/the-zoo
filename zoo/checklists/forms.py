from django.forms import widgets

from .steps import STEPS


class TagInput(widgets.TextInput):
    template_name = "checklists/fields/tag_input.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["tags"] = list(STEPS)
        context["widget"]["value"] = value

        return context
