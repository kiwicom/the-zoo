import secrets

from django.db import models


class ApiToken(models.Model):
    class Meta:
        verbose_name = "API token"

    token = models.CharField(max_length=200, unique=True, default=secrets.token_urlsafe)
    created_at = models.DateTimeField(auto_now_add=True)
    purpose = models.CharField(max_length=255, blank=False, default=None)

    def __str__(self):
        return "{}...".format(self.token[:8])  # pylint: disable=unsubscriptable-object
