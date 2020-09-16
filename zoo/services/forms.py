import itertools

from django import forms
from django.conf import settings
from django.contrib.postgres import forms as pg_forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from ..base.forms import (
    PagerdutyServiceInput,
    SentryProjectInput,
    SlackChannelInput,
    WidgetAttrsMixin,
)
from ..checklists.forms import TagInput
from ..repos.forms import RepoInput
from ..repos.github import get_namespaces as get_github_namespaces
from ..repos.gitlab import get_namespaces as get_gitlab_namespaces
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
        fields = ["name", "dashboard_url", "logs_url", "service_urls", "open_api_url"]
        labels = {
            "dashboard_url": "Dashboard URL",
            "logs_url": "Logs URL",
            "open_api_url": "OpenAPI URL",
        }


class ServiceForm(WidgetAttrsMixin, forms.ModelForm):

    namespace = "service_"
    sections = [
        {
            "title": "General",
            "subtitle": "Basic service information",
            "icon": "paperclip",
            "fields": [
                "owner",
                "name",
                "description",
                "impact",
                "status",
                "tier",
                "docs_url",
                "tags",
                "exclusions",
            ],
        },
        {
            "title": "Integrations",
            "subtitle": "Third party solutions",
            "icon": "bolt",
            "fields": [
                "repository",
                "slack_channel",
                "sentry_project",
                "sonarqube_project",
                "pagerduty_service",
            ],
        },
    ]
    exclusions = forms.CharField(
        max_length=500,
        label="Repository check exclusions",
        help_text="Comma separated paths to exclude",
        required=False,
    )

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
            "pagerduty_service",
            "docs_url",
            "tags",
        ]
        labels = {
            "docs_url": "Documentation URL",
            "sonarqube_project": "Sonarqube project key",
        }
        widgets = {
            "owner": widgets.Select(
                attrs={"class": "ui fluid search selection dropdown"},
                choices=(
                    sorted(
                        [("", "---------")]  # empty select
                        + [
                            (namespace["name"], namespace["name"])
                            for namespace in itertools.chain(
                                get_github_namespaces(), get_gitlab_namespaces()
                            )
                        ],
                        key=lambda k: k[1].lower(),
                    )
                ),
            )
            if settings.REMOTE_DATA_OWNERS
            else widgets.TextInput(),
            "repository": RepoInput(),
            "pagerduty_service": PagerdutyServiceInput(),
            "sentry_project": SentryProjectInput(),
            "slack_channel": SlackChannelInput(),
            "tags": TagInput(),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        exclusions = (
            instance.repository.exclusions if instance and instance.repository else ""
        )
        kwargs.update({"initial": {"exclusions": exclusions}})
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        try:
            repository = self.instance.repository
            if repository:
                exclusions = self.data["exclusions"]
                repository.exclusions = exclusions
                repository.save()
        except (KeyError, AttributeError):
            pass
        return super().save()


ServiceEnvironmentsFormSet = forms.inlineformset_factory(
    models.Service,
    models.Environment,
    form=EnvironmentForm,
    extra=5,
    max_num=5,
    can_delete=True,
)
