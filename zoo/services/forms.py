from django import forms
from django.forms import widgets

from . import models
from ..checklists.steps import STEPS
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


class TagInput(widgets.TextInput):
    template_name = "services/fields/tag_input.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["tags"] = list(STEPS)
        context["widget"]["value"] = value

        return context


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
            "sonarqube_project",
            "repository",
            "pagerduty_url",
            "dashboard_url",
            "docs_url",
            "service_url",
            "tags",
        ]
        labels = {
            "pagerduty_url": "PagerDuty URL",
            "dashboard_url": "Dashboard URL",
            "docs_url": "Documentation URL",
            "service_url": "Service URL",
            "sonarqube_project": "Sonarqube project Key",
        }
        widgets = {
            "repository": RepoInput(),
            "sentry_project": SentryProjectInput(),
            "tags": TagInput(),
        }
