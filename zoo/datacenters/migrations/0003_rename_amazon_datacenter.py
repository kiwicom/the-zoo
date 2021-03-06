# Generated by Django 2.2.7 on 2019-12-05 10:08

from django.db import migrations


def rename_amazon_to_aws(apps, schema_editor):
    Datacenter = apps.get_model("datacenters", "Datacenter")

    for datacenter in Datacenter.objects.all():
        if datacenter.provider == "Amazon":
            datacenter.provider = "AWS"
            datacenter.save()


def rename_aws_to_amazon(apps, schema_editor):
    Datacenter = apps.get_model("datacenters", "Datacenter")

    for datacenter in Datacenter.objects.all():
        if datacenter.provider == "AWS":
            datacenter.provider = "Amazon"
            datacenter.save()


class Migration(migrations.Migration):

    dependencies = [
        ("datacenters", "0002_auto_20191101_1019"),
    ]

    operations = [
        migrations.RunPython(rename_amazon_to_aws, reverse_code=rename_aws_to_amazon),
    ]
