import meilisearch
import structlog
from django.conf import settings
from django.core.management.base import BaseCommand

log = structlog.get_logger()


class Command(BaseCommand):
    help = "Create initial MeiliSearch indexes"

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument(
            "-d", "--delete", action="store_true", help="Delete indexes"
        )
        parser.add_argument(
            "-r", "--recreate", action="store_true", help="Recreate indexes"
        )

    def handle(self, *args, **options):
        delete = options["delete"]
        recreate = options["recreate"]

        client = meilisearch.Client(settings.MEILI_HOST, settings.MEILI_MASTER_KEY)

        if delete:
            Command._delete_indexes(client)
            return

        if recreate:
            Command._delete_indexes(client)
            Command._create_indexes(client)
            return

        Command._create_indexes(client)

    @staticmethod
    def _create_indexes(client):
        try:
            client.create_index(
                uid="services", options={"name": "Service", "primaryKey": "id"}
            )
            log.info("globalsearch.commands.create_indexes.services.success")
            client.create_index(
                uid="analytics", options={"name": "Dependency", "primaryKey": "id"}
            )
            log.info("globalsearch.commands.create_indexes.analytics.success")
            client.create_index(
                uid="open-api", options={"name": "Schema", "primaryKey": "id"}
            )
            log.info("globalsearch.commands.create_indexes.open-api.success")
        except meilisearch.errors.MeiliSearchApiError as e:
            log.error("globalsearch.commands.create_indexes.error")
            log.error(e)
            return
        log.info("globalsearch.commands.create_indexes.success")

    @staticmethod
    def _delete_indexes(client):
        try:
            client.index("services").delete()
            log.info("globalsearch.commands.delete_indexes.services.success")
            client.index("analytics").delete()
            log.info("globalsearch.commands.delete_indexes.analytics.success")
            client.index("open-api").delete()
            log.info("globalsearch.commands.delete_indexes.open-api.success")
        except meilisearch.errors.MeiliSearchApiError as e:
            log.error("globalsearch.commands.delete_indexes.success.error")
            log.error(e)
            return
        log.info("globalsearch.commands.delete_indexes.success")
