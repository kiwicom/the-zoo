# Generated by Django 2.2.9 on 2020-01-20 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0014_add_environment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="slack_channel",
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
