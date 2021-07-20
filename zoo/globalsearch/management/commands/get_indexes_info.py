import meilisearch
import structlog
from django.conf import settings
from django.core.management.base import BaseCommand

log = structlog.get_logger()


class Command(BaseCommand):
    help = "List MeiliSearch indexes"

    def handle(self, *args, **options):

        client = meilisearch.Client(settings.MEILI_HOST, settings.MEILI_MASTER_KEY)

        indexes = client.get_indexes()

        log.info(indexes)
