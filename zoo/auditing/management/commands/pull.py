from django.core.management.base import BaseCommand

from ....repos.tasks import pull


class Command(BaseCommand):
    help = "Pulls the specific repo and perform the checks"

    def add_arguments(self, parser):
        parser.add_argument("repo_id")
        parser.add_argument("provider")

    def handle(self, *args, **options):
        repo_id = options["repo_id"]
        provider = options["provider"]
        pull(repo_id, provider)
