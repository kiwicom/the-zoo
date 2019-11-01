import sys

import django
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ... import settings
from ....services.models import Service, Status


class Command(BaseCommand):
    help = "Fake data for local dev + creates superuser."

    def handle(self, *args, **options):
        # todo - is this worth ?
        if settings.DATABASES["default"]["PASSWORD"] != "postgres":
            print("You're not on localhost, nothings happening.")
            sys.exit(1)

        # todo - use faker, create more data ?
        s = Service(
            owner="jake",
            name="my-service",
            status=Status.PRODUCTION,
            slack_channel="#plz-hello",
        )
        try:
            s.save()
        except django.db.utils.IntegrityError:
            print(f"'{s}' already exists, skipping creation.")
        else:
            print("Created 1 service.")

        try:
            User = get_user_model()
            User.objects.create_superuser("admin", "admin@myproject.com", "password")
        except:
            print(f"Admin, already exists, skipping creation.")
        else:
            print("Created superuser 'admin/password'.")
