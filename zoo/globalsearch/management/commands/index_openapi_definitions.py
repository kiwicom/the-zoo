from django.core.management.base import BaseCommand

from zoo.globalsearch.tasks import index_openapi_definitions


class Command(BaseCommand):
    help = "Indexes open api defintions"

    def handle(self, *args, **options):
        index_openapi_definitions()
