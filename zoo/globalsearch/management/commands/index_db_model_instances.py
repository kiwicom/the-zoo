from django.core.management.base import BaseCommand

from zoo.globalsearch.tasks import index_db_model_instances


class Command(BaseCommand):
    help = "Indexes database model instances"

    def handle(self, *args, **options):
        index_db_model_instances()
