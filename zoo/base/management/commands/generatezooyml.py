from django.core.management.base import BaseCommand

from zoo.repos import github, gitlab, zoo_yml
from zoo.repos.models import Repository
from zoo.services.models import Service


class Command(BaseCommand):
    help = "generate .zoo.yml file for all services in the database that do not have it"

    ZOO_YML = ".zoo.yml"
    ZOO_COMMIT_MSG = "feat(zoo): generate .zoo.yml file"

    def handle(self, *args, **options):
        for service in Service.objects.all():
            remote_id, provider = (
                service.repository.remote_id,
                self.get_provider(service.repository.provider),
            )
            if not provider:
                continue

            if self.file_exists(remote_id, Command.ZOO_YML, provider):
                continue

            yml = zoo_yml.generate(service)
            actions = [
                {"action": "create", "content": yml, "file_path": Command.ZOO_YML}
            ]
            branch = "master"

            provider.create_remote_commit(
                remote_id, Command.ZOO_COMMIT_MSG, actions, branch, provider
            )

    def get_provider(self, provider):
        providers = {
            "github": github,
            "gitlab": gitlab,
        }

        return providers[provider]

    def file_exists(self, remote_id, path, provider, ref="master"):
        try:
            content = provider.get_file_content(remote_id, path, ref)
            if not content:
                return False
            return True
        except FileNotFoundError:
            return False
