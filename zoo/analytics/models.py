from collections import Counter
from enum import Enum

from django.db import models
from django.utils import timezone


class DependencyType(Enum):
    LANG = "Language"
    OS = "Operating System"
    JS_LIB = "Javascript Library"
    PY_LIB = "Python Library"
    GO_LIB = "Go Library"
    RS_LIB = "Rust Library"
    ER_LIB = "Erlang Library"
    DOCKER_IMG = "Docker Image"
    GITLAB_CI = "Gitlab-ci.yml"


class NameField(models.CharField):
    def get_prep_value(self, value):
        return str(value).lower()


class Dependency(models.Model):
    class Meta:
        unique_together = ("name", "type")
        verbose_name_plural = "dependencies"

    name = NameField(max_length=1000)
    type = models.CharField(
        max_length=100, choices=((item.value, item.value) for item in DependencyType)
    )
    health_status = models.NullBooleanField(
        null=True, blank=True, default=None, verbose_name="health"
    )
    timestamp = models.DateTimeField(default=timezone.now)
    license = models.CharField(max_length=10000, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class DependencySnapshot(models.Model):
    class Meta:
        unique_together = ("dependency", "timestamp")

    dependency = models.ForeignKey(
        Dependency, on_delete=models.PROTECT, related_name="snapshots"
    )
    timestamp = models.DateTimeField(default=timezone.now)
    dep_usages_num = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.dependency} at ({self.timestamp})"


class DependencyUsage(models.Model):
    class Meta:
        unique_together = ("dependency", "repo")

    dependency = models.ForeignKey(
        Dependency, on_delete=models.CASCADE, related_name="depusage"
    )
    repo = models.ForeignKey("repos.Repository", on_delete=models.CASCADE)
    major_version = models.BigIntegerField(null=True, blank=True)
    minor_version = models.BigIntegerField(null=True, blank=True)
    patch_version = models.BigIntegerField(null=True, blank=True)
    version = models.CharField(max_length=200, null=True, blank=True)
    for_production = models.NullBooleanField(
        null=True, blank=True, verbose_name="production"
    )
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.repo}'s {self.dependency.name}" + (
            f" v{self.version}" if self.version else ""
        )

    @staticmethod
    def versions(queryset, limit=None):
        queryset = queryset.exclude(version__isnull=True)
        counter = Counter(queryset.values_list("version", flat=True))
        return sorted(counter.most_common(n=limit), key=lambda t: t[0], reverse=True)
