# Generated by Django 2.1.3 on 2018-11-27 15:16

import django.contrib.postgres.fields
from django.db import migrations, models


def add_default_general_tag(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    for service in Service.objects.all():
        service.tags = ["general"]
        service.save()


class Migration(migrations.Migration):

    dependencies = [("services", "0010_service_ci_unique_fields")]

    operations = [
        migrations.AddField(
            model_name="service",
            name="tags",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=list,
                size=None,
            ),
        ),
        migrations.RunPython(add_default_general_tag),
    ]
