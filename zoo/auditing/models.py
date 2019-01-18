from enum import Enum

from django.contrib.postgres import fields as pg_fields
from django.db import models
from django.utils import timezone
import markdown

from ..repos.models import Repository
from .check_discovery import KINDS


class Issue(models.Model):
    class Status(Enum):
        NEW = "new"
        FIXED = "fixed"
        WONTFIX = "wontfix"
        NOT_FOUND = "not found"
        REOPENED = "reopened"

    repository = models.ForeignKey(
        Repository, on_delete=models.CASCADE, related_name="issues"
    )
    kind_key = models.CharField(max_length=500)
    status = models.CharField(
        choices=((item.value, item.value) for item in Status),
        default=Status.NEW.value,
        max_length=100,
    )
    details = pg_fields.JSONField(default=dict, blank=True)
    remote_issue_id = models.PositiveIntegerField(null=True, blank=True)
    merge_request_id = models.PositiveIntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    last_check = models.DateTimeField(default=timezone.now)
    deleted = models.BooleanField(default=False)

    @property
    def kind(self):
        return KINDS[self.kind_key]

    @property
    def description_md(self):
        return self.kind.format_description(self.details)

    @property
    def description_html(self):
        return markdown.markdown(
            self.description_md,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.smarty",
            ],
        )

    @property
    def remote_issue_url(self):
        return f"{self.repository.url}/issues/{self.remote_issue_id}"

    @property
    def merge_request(self):
        return {
            "id": self.merge_request_id,
            "url": self.repository.get_merge_request_url(self.merge_request_id),
            "label": self.repository.get_merge_request_label(self.merge_request_id),
        }

    def __str__(self):
        return f"{self.kind} issue on {self.repository}"


class IssueCountByRepositorySnapshot(models.Model):
    class Meta:
        unique_together = ("repository", "timestamp")

    repository = models.ForeignKey(
        Repository, on_delete=models.CASCADE, related_name="issue_count_snapshots"
    )
    status = models.CharField(
        choices=((item.value, item.value) for item in Issue.Status), max_length=100
    )
    timestamp = models.DateTimeField(default=timezone.now)
    count = models.PositiveIntegerField()


class IssueCountByKindSnapshot(models.Model):
    class Meta:
        unique_together = ("kind_key", "timestamp")

    kind_key = models.CharField(max_length=500)
    status = models.CharField(
        choices=((item.value, item.value) for item in Issue.Status), max_length=100
    )
    timestamp = models.DateTimeField(default=timezone.now)
    count = models.PositiveIntegerField()
