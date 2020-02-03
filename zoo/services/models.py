import re
from collections import OrderedDict, namedtuple
from enum import Enum

import arrow
from django.conf import settings
from django.contrib.postgres import fields as pg_fields
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from djangoql.schema import DjangoQLSchema

from . import ratings


class Status(Enum):
    BETA = "beta"
    PRODUCTION = "production"
    DEPRECATED = "deprecated"
    DISCONTINUED = "discontinued"


class Impact(Enum):
    PROFIT = "profit"
    CUSTOMERS = "customers"
    EMPLOYEES = "employees"


class Service(models.Model):
    class Meta:
        unique_together = ("owner", "name")

    owner = pg_fields.CICharField(max_length=100)
    name = pg_fields.CICharField(max_length=100)
    status = models.CharField(
        choices=((item.value, item.value) for item in Status),
        null=True,
        blank=True,
        max_length=100,
    )
    impact = models.CharField(
        choices=((item.value, item.value) for item in Impact),
        null=True,
        blank=True,
        max_length=100,
    )
    slack_channel = models.CharField(max_length=80, null=True, blank=True)
    sentry_project = models.CharField(max_length=100, null=True, blank=True)
    sonarqube_project = models.CharField(max_length=250, null=True, blank=True)
    rating_grade = models.CharField(max_length=1, null=True, blank=True)
    rating_reason = models.CharField(max_length=250, null=True, blank=True)
    repository = models.ForeignKey(
        "repos.Repository",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="services",
    )
    pagerduty_url = models.URLField(max_length=500, null=True, blank=True)
    docs_url = models.URLField(max_length=500, null=True, blank=True)
    owner_slug = models.SlugField(max_length=140)
    name_slug = models.SlugField(max_length=140)
    tags = pg_fields.ArrayField(
        base_field=models.CharField(max_length=50), blank=True, default=list
    )

    def get_absolute_url(self):
        return reverse("service_detail", args=[self.owner_slug, self.name_slug])

    def rate_according_to_sentry(self):
        Category = SentryIssueCategory
        queryset = self.sentry_issues.prefetch_related("stats").all()

        if not queryset.exists():
            return {
                "grade": "S",
                "reason": "No issues at all 🎉 You, my friends, are doing an amazing job 😎",
            }

        three_days_ago = arrow.now().shift(days=-3).day
        is_recent = models.Q(stats__timestamp__day__gte=three_days_ago)
        queryset = queryset.annotate(freq=models.Sum("stats__count", filter=is_recent))

        avg_daily_events_count = queryset.aggregate(models.Sum("freq"))["freq__sum"] / 3

        issues = SentryIssueCounts(
            total=queryset.count(),
            problematic=queryset.exclude(category=Category.FRESH.value).count(),
            spoiled=queryset.filter(category=Category.SPOILED.value).count(),
            decaying=queryset.filter(category=Category.DECAYING.value).count(),
            stale=queryset.filter(category=Category.STALE.value).count(),
        )

        return ratings.SentryRater(avg_daily_events_count, issues).get_rating()

    def update_rating(self):
        sentry_rating = self.rate_according_to_sentry() if self.sentry_project else None

        if sentry_rating:
            self.rating_grade = sentry_rating["grade"]
            self.rating_reason = sentry_rating["reason"]
            self.full_clean()
            self.save()

    def get_environment(self, name=None):
        if name is None:
            return self.environments.first()
        return self.environments_dict.get(name)

    @property
    def key(self):
        return f"{self.owner}/{self.name}"

    @property
    def owner_url(self):
        if self.repository:
            return f"{settings.GITLAB_URL}/{self.repository.owner}"

    @property
    def service_url(self):
        default_env = self.get_environment()
        if default_env and default_env.service_urls:
            return default_env.service_urls[0]

    @property
    def slack_url(self):
        if self.slack_channel:
            return f"{settings.SLACK_URL}/messages/{self.slack_channel}"

    @property
    def gitlab_url(self):
        if self.repository:
            return (
                f"{settings.GITLAB_URL}/{self.repository.owner}/{self.repository.name}"
            )

    @property
    def pagerduty_service_id(self):
        if self.pagerduty_url is None:
            return

        service_re = re.search(
            r"pagerduty.com\/services\/([A-Z0-9]+)", self.pagerduty_url
        )
        if service_re:
            return service_re.group(1)

    @property
    def environments_dict(self):
        return OrderedDict(
            (env.name, env) for env in self.environments.order_by("id").all()
        )

    def __str__(self):
        return f"{self.key}"


class Environment(models.Model):
    class Meta:
        unique_together = ("service", "name")

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="environments",
        related_query_name="environment",
    )
    name = models.CharField(max_length=100)
    service_urls = pg_fields.ArrayField(
        models.URLField(max_length=500), null=True, default=list
    )
    health_check_url = models.URLField(max_length=500, null=True, blank=True)
    dashboard_url = models.URLField(max_length=500, null=True, blank=True)
    logs_url = models.URLField(max_length=500, null=True, blank=True)


def slugify_attribute(attribute):
    return re.sub("[^0-9a-zA-Z]+", "-", attribute)


@receiver(models.signals.pre_save, sender=Service)
def generate_slugs(sender, instance, *args, **kwargs):
    instance.owner_slug = slugify_attribute(instance.owner)
    instance.name_slug = slugify_attribute(instance.name)


@receiver(models.signals.pre_save, sender=Service)
def generate_tags(sender, instance, *args, **kwargs):
    if "general" not in instance.tags:
        instance.tags.append("general")


class SentryIssueCategory(Enum):
    STALE = "stale"
    DECAYING = "decaying"
    SPOILED = "spoiled"
    FRESH = "fresh"


SentryIssueCounts = namedtuple(
    "SentryIssueCounts", ["total", "problematic", "spoiled", "decaying", "stale"]
)


class SentryIssue(models.Model):
    title = models.CharField(max_length=300)
    culprit = models.CharField(max_length=200, blank=True)
    short_id = models.CharField(max_length=250)
    issue_id = models.IntegerField()
    assignee = models.CharField(max_length=50, null=True, blank=True)
    permalink = models.URLField(max_length=500)
    events = models.IntegerField()
    users = models.IntegerField()
    first_seen = models.DateTimeField()
    last_seen = models.DateTimeField()
    service = models.ForeignKey(
        "services.Service", on_delete=models.CASCADE, related_name="sentry_issues"
    )
    category = models.CharField(
        choices=((item.value, item.value) for item in SentryIssueCategory),
        null=True,
        blank=True,
        max_length=100,
    )


class SentryIssueStats(models.Model):
    class Meta:
        unique_together = ("timestamp", "issue")
        verbose_name_plural = "sentry issue stats"

    timestamp = models.DateTimeField()
    count = models.IntegerField()
    issue = models.ForeignKey(
        "services.SentryIssue", on_delete=models.CASCADE, related_name="stats"
    )


class ServiceQLSchema(DjangoQLSchema):
    include = (Service, Environment)

    def get_fields(self, model):
        if isinstance(model, Service):
            return ["name", "owner", "status", "impact"]
        if isinstance(model, Environment):
            return ["service_urls", "health_check_url"]
        return super(ServiceQLSchema, self).get_fields(model)
