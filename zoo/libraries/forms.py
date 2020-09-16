from django import forms

from ..checklists.forms import TagInput
from ..repos.forms import RepoInput
from . import models


class LibraryForm(forms.ModelForm):
    namespace = "library_"
    sections = [
        {
            "title": "General",
            "subtitle": "Basic service information",
            "icon": "paperclip",
            "fields": ["owner", "name", "impact", "status", "docs_url", "tags"],
        },
        {
            "subtitle": "Third party solutions",
            "icon": "bolt",
            "fields": ["repository", "slack_channel", "sonarqube_project"],
        },
    ]

    class Meta:
        model = models.Library
        fields = [
            "owner",
            "name",
            "impact",
            "status",
            "slack_channel",
            "sonarqube_project",
            "repository",
            "docs_url",
            "library_url",
            "tags",
        ]
        labels = {
            "docs_url": "Documentation URL",
            "library_url": "Library URL",
            "sonarqube_project": "Sonarqube project Key",
        }
        widgets = {"repository": RepoInput(), "tags": TagInput()}
