from django import forms
from django.contrib.postgres import forms as pg_forms
from django.core.exceptions import ValidationError

from ..base.forms import (
    PagerdutyServiceInput,
    SentryProjectInput,
    SlackChannelInput,
    WidgetAttrsMixin,
)
from ..checklists.forms import TagInput
from ..repos.forms import RepoInput
from . import models


class SplitArrayField(pg_forms.SplitArrayField):
    def has_changed(self, initial, data):
        try:
            python_data = self.to_python(data)
        except ValidationError:
            pass
        else:
            if self.remove_trailing_nulls:
                null_index = None
                for i, value in reversed(list(enumerate(python_data))):
                    if value in self.base_field.empty_values:
                        null_index = i
                    else:
                        break
                if null_index is not None:
                    data = python_data[:null_index]

        if initial in self.empty_values and data in self.empty_values:
            return False
        return super().has_changed(initial, data)


class EnvironmentForm(forms.ModelForm):
    service_urls = SplitArrayField(
        forms.URLField(required=False),
        size=5,
        remove_trailing_nulls=True,
        label="Service URLs",
        required=False,
    )

    class Meta:
        model = models.Environment
        fields = ["name", "dashboard_url", "logs_url", "service_urls"]
        labels = {"dashboard_url": "Dashboard URL", "logs_url": "Logs URL"}


class ServiceForm(WidgetAttrsMixin, forms.ModelForm):
    class Meta:
        model = models.Service
        fields = [
            "owner",
            "name",
            "description",
            "impact",
            "status",
            "tier",
            "slack_channel",
            "sentry_project",
            "sonarqube_project",
            "repository",
            "pagerduty_url",
            "pagerduty_service",
            "docs_url",
            "tags",
        ]
        labels = {
            "docs_url": "Documentation URL",
            "sonarqube_project": "Sonarqube project key",
        }
        _placeholders = {
            "name": "New cool service",
        }
        widgets = {
            "repository": RepoInput(),
            "pagerduty_service": PagerdutyServiceInput(),
            "sentry_project": SentryProjectInput(),
            "slack_channel": SlackChannelInput(),
            "tags": TagInput(),
        }


ServiceEnvironmentsFormSet = forms.inlineformset_factory(
    models.Service,
    models.Environment,
    form=EnvironmentForm,
    extra=5,
    max_num=5,
    can_delete=True,
)
