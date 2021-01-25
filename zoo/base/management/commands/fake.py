import sys

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from ....factories import ApiTokenFactory, ServiceFactory
from ... import settings


class Command(BaseCommand):
    help = "Fake data for local dev + creates superuser."

    def add_arguments(self, parser):
        parser.add_argument("amount", nargs="?", type=int, default=50)

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write(
                "Not creating fake data because environment variable ZOO_DEBUG is False."
            )
            sys.exit(1)

        try:
            User = get_user_model()
            User.objects.create_superuser("admin", "", "password")
        except IntegrityError:
            self.stdout.write("Admin, already exists, skipping creation.")
        else:
            self.stdout.write(self.style.SUCCESS("Created superuser 'admin/password'."))

        ServiceFactory.create_batch(options["amount"])
        self.stdout.write(self.style.SUCCESS(f'{options["amount"]} services created.'))

        auth = ApiTokenFactory.create()
        self.stdout.write(
            self.style.SUCCESS(f"graphql api token {auth.token} created.")
        )
