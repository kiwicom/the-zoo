# Generated by Django 2.2.16 on 2020-09-07 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0018_environment_open_api"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="environment",
            options={"ordering": ["name"]},
        ),
    ]
