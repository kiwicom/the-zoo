from django import forms

from . import models
from ..base.forms import SentryProjectInput
from ..checklists.forms import TagInput
from ..repos.forms import RepoInput


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
