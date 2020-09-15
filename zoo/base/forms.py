from django.forms import widgets

from ..instance.models import Helpers, Placeholders


class WidgetAttrsMixin:
    """ModelForm mixin to overwrite Widget attrs like placeholder."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._metadata_hook()

    def _metadata_hook(self):
        helpers = Helpers.resolve()
        placeholders = Placeholders.resolve()

        for field in self.fields:
            self.fields[field].help_text = (
                getattr(helpers, f"{self.namespace}{field}", "")
                or self.fields[field].help_text
            )

            widget = self.fields[field].widget
            widget.attrs.update(
                {
                    "placeholder": (
                        getattr(placeholders, f"{self.namespace}{field}", "")
                        or widget.attrs.get("placeholder", "")
                    )
                }
            )


class PagerdutyServiceInput(widgets.TextInput):
    template_name = "shared/fields/pagerduty_input.html"


class SentryProjectInput(widgets.TextInput):
    template_name = "shared/fields/sentry_input.html"


class SlackChannelInput(widgets.TextInput):
    template_name = "shared/fields/slack_input.html"
