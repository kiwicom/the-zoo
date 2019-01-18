from enum import Enum

from django.db import models

from ..analytics.models import Dependency
from .utils import get_scm_module


class Provider(Enum):
    GITLAB = "gitlab"
    GITHUB = "github"


class Repository(models.Model):
    class Meta:
        unique_together = ("remote_id", "provider", "owner", "name")
        verbose_name_plural = "repositories"

    remote_id = models.IntegerField()
    provider = models.CharField(
        choices=((item.value, item.value) for item in Provider), max_length=100
    )
    owner = models.CharField(max_length=100, db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    url = models.URLField(max_length=500)

    def __str__(self):
        return f"{self.owner}/{self.name}"

    @property
    def scm_module(self):
        return get_scm_module(self.provider)

    @property
    def remote_git_object(self):
        return self.scm_module.get_project(self.remote_id)

    @property
    def languages_from_analytics(self):
        return list(
            Dependency.objects.filter(type="Language", depusage__repo=self).values_list(
                "name", flat=True
            )
        )

    def get_merge_request_url(self, mr_id):
        return {
            Provider.GITLAB.value: f"{self.url}/merge_requests/{mr_id}",
            Provider.GITHUB.value: f"{self.url}/pull/{mr_id}",
        }[self.provider]

    def get_merge_request_label(self, mr_id):
        return {
            Provider.GITLAB.value: f"Merge Request #{mr_id}",
            Provider.GITHUB.value: f"Pull Request #{mr_id}",
        }[self.provider]
