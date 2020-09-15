import structlog
from django.db import models

log = structlog.get_logger()

INSTANCE_ID = 1


class Singleton(models.Model):
    instance_id = INSTANCE_ID
    cache_name = "singleton"

    class Meta:
        abstract = True

    def __str__(self):
        return "Config"

    @classmethod
    def resolve(cls):
        return cls.objects.get_or_create(pk=cls.instance_id)[0]


class Hints(Singleton):
    class Meta:
        verbose_name_plural = "hints"

    library_form_explanation = models.TextField(max_length=1500)
    service_form_explanation = models.TextField(max_length=1500)


class Placeholders(Singleton):
    class Meta:
        verbose_name_plural = "placeholders"

    service_description = models.CharField(max_length=250, null=True, blank=True)
    service_docs_url = models.CharField(max_length=250, null=True, blank=True)
    service_exclusions = models.CharField(max_length=250, null=True, blank=True)
    service_impact = models.CharField(max_length=250, null=True, blank=True)
    service_name = models.CharField(max_length=250, null=True, blank=True)
    service_owner = models.CharField(max_length=250, null=True, blank=True)
    service_pagerduty_service = models.CharField(max_length=250, null=True, blank=True)
    service_repository = models.CharField(max_length=250, null=True, blank=True)
    service_sentry_project = models.CharField(max_length=250, null=True, blank=True)
    service_slack_channel = models.CharField(max_length=250, null=True, blank=True)
    service_sonarqube_project = models.CharField(max_length=250, null=True, blank=True)
    service_status = models.CharField(max_length=250, null=True, blank=True)
    service_tags = models.CharField(max_length=250, null=True, blank=True)
    service_tier = models.CharField(max_length=250, null=True, blank=True)


class Helpers(Singleton):
    class Meta:
        verbose_name_plural = "helpers"

    service_description = models.CharField(max_length=250, null=True, blank=True)
    service_docs_url = models.CharField(max_length=250, null=True, blank=True)
    service_exclusions = models.CharField(max_length=250, null=True, blank=True)
    service_impact = models.CharField(max_length=250, null=True, blank=True)
    service_name = models.CharField(max_length=250, null=True, blank=True)
    service_owner = models.CharField(max_length=250, null=True, blank=True)
    service_pagerduty_service = models.CharField(max_length=250, null=True, blank=True)
    service_repository = models.CharField(max_length=250, null=True, blank=True)
    service_sentry_project = models.CharField(max_length=250, null=True, blank=True)
    service_slack_channel = models.CharField(max_length=250, null=True, blank=True)
    service_sonarqube_project = models.CharField(max_length=250, null=True, blank=True)
    service_status = models.CharField(max_length=250, null=True, blank=True)
    service_tags = models.CharField(max_length=250, null=True, blank=True)
    service_tier = models.CharField(max_length=250, null=True, blank=True)
