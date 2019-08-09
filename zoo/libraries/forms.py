from django import forms

from . import models
from ..checklists.forms import TagInput
from ..repos.forms import RepoInput


class LibraryForm(forms.ModelForm):
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
