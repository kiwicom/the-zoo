# Generated by Django 2.2.12 on 2020-07-15 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="apitoken",
            options={"verbose_name": "API token"},
        ),
    ]
