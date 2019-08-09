from django.forms import widgets


class SentryProjectInput(widgets.TextInput):
    template_name = "shared/fields/sentry_input.html"
