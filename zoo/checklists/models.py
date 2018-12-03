from django.db import models
from django.utils import timezone


class Checkmark(models.Model):
    class Meta:
        unique_together = ("service", "step_key")

    service = models.ForeignKey(
        "services.Service", on_delete=models.PROTECT, related_name="checkmarks"
    )
    step_key = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
