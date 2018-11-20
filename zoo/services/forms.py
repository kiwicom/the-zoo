from django import forms
from django.forms import widgets

from . import models
from ..repos.models import Repository


class RepoInput(widgets.TextInput):
    template_name = "services/fields/repo_input.html"

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


class SentryProjectInput(widgets.TextInput):
    template_name = "services/fields/sentry_input.html"


class ServiceForm(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = [
            "owner",
            "name",
            "impact",
            "status",
            "slack_channel",
            "sentry_project",
            "datacenter",
            "repository",
            "pagerduty_url",
            "dashboard_url",
            "docs_url",
            "service_url",
        ]
        labels = {
            "pagerduty_url": "PagerDuty URL",
            "dashboard_url": "Dashboard URL",
            "docs_url": "Documentation URL",
            "service_url": "Service URL",
        }
        widgets = {"repository": RepoInput(), "sentry_project": SentryProjectInput()}
