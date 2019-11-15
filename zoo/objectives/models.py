import operator
from enum import Enum

import structlog
from django.db import models
from django.utils import timezone

log = structlog.get_logger()


class IndicatorSource(Enum):
    DATADOG = "datadog"
    PINGDOM = "pingdom"


class ObjectiveTargetType(Enum):
    ABOVE = "above"
    BELOW = "below"


class Objective(models.Model):
    class Meta:
        unique_together = ("service", "indicator_source", "indicator_query")

    service = models.ForeignKey("services.Service", on_delete=models.PROTECT)
    indicator_source = models.CharField(
        choices=((item.value, item.value) for item in IndicatorSource), max_length=100
    )
    indicator_query = models.CharField(max_length=10000)
    target = models.DecimalField(max_digits=12, decimal_places=4)
    target_type = models.CharField(
        choices=((item.value, item.value) for item in ObjectiveTargetType),
        null=True,
        blank=True,
        max_length=100,
    )

    @property
    def meets_target(self) -> bool:
        comparison = operator.gt if self.target_type == "above" else operator.lt
        if self.latest_value:
            return comparison(self.latest_value.indicator_value, self.target)
        return False

    @property
    def check_url(self):
        if self.indicator_source == "pingdom":
            return f"https://my.pingdom.com/reports/uptime#check={self.indicator_query}"

    @property
    def latest_value(self):
        return self.snapshots.latest("timestamp") if self.snapshots.exists() else None


class ObjectiveSnapshot(models.Model):
    class Meta:
        unique_together = ("objective", "timestamp")

    objective = models.ForeignKey(
        Objective, on_delete=models.PROTECT, related_name="snapshots"
    )
    timestamp = models.DateTimeField(default=timezone.now)
    indicator_value = models.DecimalField(max_digits=12, decimal_places=4)
