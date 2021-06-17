from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres import fields as pg_fields
from django.db import models


class Group(models.Model):
    product_owner = models.CharField(max_length=100)
    project_owner = models.CharField(max_length=100)
    maintainers = pg_fields.ArrayField(
        base_field=models.CharField(max_length=50),
        default=list,
        help_text="List of maintainers",
    )


class Link(models.Model):
    name = models.CharField(max_length=32)
    icon = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        help_text="https://fomantic-ui.com/elements/icon.html",
    )
    url = models.URLField()
    component = models.ForeignKey(
        "components.Component",
        related_name="links",
        related_query_name="link",
        on_delete=models.PROTECT,
    )


class Component(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=32)
    description = models.CharField(max_length=255, null=True, blank=True)
    kind = models.CharField(max_length=16)
    owner = models.CharField(max_length=50)
    group = models.OneToOneField(
        "components.Group",
        related_name="components",
        related_query_name="component",
        on_delete=models.PROTECT,
    )
    tags = pg_fields.ArrayField(
        base_field=models.CharField(max_length=50),
        blank=True,
        default=list,
        help_text="Used for filtering and defining presets of checks",
    )
    source = models.ForeignKey(
        "repos.Repository",
        related_name="components",
        related_query_name="component",
        on_delete=models.PROTECT,
    )
    service = models.OneToOneField(
        "services.Service", on_delete=models.PROTECT, null=True, blank=True
    )
    library = models.OneToOneField(
        "libraries.Library", on_delete=models.PROTECT, null=True, blank=True
    )
