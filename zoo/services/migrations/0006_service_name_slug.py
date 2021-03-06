# Generated by Django 2.1 on 2018-08-20 13:53

import re

from django.db import migrations, models


def generate_name_slug(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    for service in Service.objects.all():
        service.name_slug = re.sub("[^0-9a-zA-Z]+", "-", service.name)
        service.full_clean()
        service.save()


class Migration(migrations.Migration):

    dependencies = [("services", "0005_service_owner_slug")]

    operations = [
        migrations.AddField(
            model_name="service",
            name="name_slug",
            field=models.SlugField(default="", max_length=140),
            preserve_default=False,
        ),
        migrations.RunPython(generate_name_slug),
    ]
