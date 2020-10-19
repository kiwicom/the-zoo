import meilisearch
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create initial MeiliSearch indexes"

    def handle(self, *args, **options):
        client = meilisearch.Client(settings.MEILI_HOST, settings.MEILI_MASTER_KEY)
        client.create_index(
            uid="services", options={"name": "Service", "primaryKey": "id"}
        )
        client.create_index(
            uid="analytics", options={"name": "Dependency", "primaryKey": "id"}
        )
        client.create_index(
            uid="open-api", options={"name": "Schema", "primaryKey": "id"}
        )
