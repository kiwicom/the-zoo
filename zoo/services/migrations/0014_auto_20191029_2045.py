# Generated by Django 2.2.6 on 2019-10-29 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0013_auto_20190515_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='repository',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='services', to='repos.Repository'),
        ),
    ]
