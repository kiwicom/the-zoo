from django.forms import widgets


class WidgetAttrsMixin:
    """ModelForm mixin to overwrite Widget attrs like placeholder."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._placeholder_hook()

    def _placeholder_hook(self):
        placeholders = getattr(self.Meta, "_placeholders", {})
        for field, placeholder in placeholders.items():
            widget = self.fields[field].widget
            widget.attrs = {**widget.attrs, **{"placeholder": placeholder}}


class SentryProjectInput(widgets.TextInput):
    template_name = "shared/fields/sentry_input.html"


class SlackChannelInput(widgets.TextInput):
    template_name = "shared/fields/slack_input.html"
