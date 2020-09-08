import hashlib
import itertools
import tempfile
from typing import Dict

import structlog
from celery import shared_task
from django.conf import settings

from ..analytics.tasks import repo_analyzers
from ..auditing import runner
from ..auditing.check_discovery import CHECKS as AUDITING_CHECKS
from ..services.models import Environment, Service
from .exceptions import MissingFilesError, RepositoryNotFoundError
from .github import get_repositories as get_github_repositories
from .gitlab import get_repositories as get_gitlab_repositories
from .models import Repository
from .utils import download_repository, get_scm_module
from .zoo_yml import parse, validate

log = structlog.get_logger()


@shared_task
def sync_repos():
    for project in itertools.chain(
        get_github_repositories(), get_gitlab_repositories()
    ):
        if settings.SYNC_REPOS_SKIP_FORKS and project["is_fork"]:
            continue
        if settings.SYNC_REPOS_SKIP_PERSONAL and project["is_personal"]:
            continue

        try:
            repo = Repository.objects.get(
                remote_id=project["id"], provider=project["provider"]
            )
        except Repository.DoesNotExist:
            try:
                repo = Repository.objects.get(
                    owner=project["owner"],
                    name=project["name"],
                    provider=project["provider"],
                )
                repo.remote_id = project["id"]
            except Repository.DoesNotExist:
                repo = Repository(remote_id=project["id"], provider=project["provider"])

        repo.owner = project["owner"]
        repo.name = project["name"]
        repo.url = project["url"]
        repo.full_clean()
        repo.save()


@shared_task
def schedule_pulls():
    """Create one pull task per repo."""
    for repo in Repository.objects.all():
        # distribute pulls by delaying evenly across an hour
        pk_hash = hashlib.sha256(str(repo.pk).encode())
        delay_s = int(pk_hash.hexdigest(), 16) % (60 * 60)

        pull.apply_async(
            args=(repo.remote_id, repo.provider),
            countdown=delay_s,
            expires=delay_s + (60 * 60),
        )


@shared_task
def pull(reference, provider):
    """Run all repo tasks on one repo."""
    try:
        repository = Repository.objects.get(remote_id=int(reference), provider=provider)
    except ValueError:
        owner, name = reference.rsplit("/", 1)
        repository = Repository.objects.get(owner=owner, name=name, provider=provider)

    log.info("repos.pull", repo=repository)

    with tempfile.TemporaryDirectory() as repo_dir:
        try:
            repo_path = download_repository(repository, repo_dir)
        except (MissingFilesError, RepositoryNotFoundError) as err:
            log.info("repos.pull.git_error", repo=repository, error=err)
            return

        repo_analyzers.run_all(repository, repo_path)
        runner.run_checks_and_save_results(AUDITING_CHECKS, repository, repo_path)


@shared_task
def sync_zoo_file():
    for project in itertools.chain(
        get_github_repositories(), get_gitlab_repositories()
    ):
        if settings.SYNC_REPOS_SKIP_FORKS and project["is_fork"]:
            continue
        update_project_from_zoo_file.apply_async(args=project)


@shared_task
def update_project_from_zoo_file(proj: Dict) -> None:
    try:
        content = get_zoo_file_content(proj)
    except FileNotFoundError as err:
        log.info("repos.sync_zoo_yml.file_not_found", error=err)
    else:
        if not validate(content):
            return
        update_or_create_service(parse(content), proj)


def update_or_create_service(data: Dict, proj: Dict) -> None:
    # Skip processing the zoo file if the repository is not yet synced
    try:
        repository = Repository.objects.get(
            remote_id=int(proj["id"]), provider=proj["provider"]
        )
    except Repository.DoesNotExist:
        return

    service_defaults = {
        "impact": data["impact"],
        "status": data["status"],
        "repository": repository,
        "docs_url": data["docs_url"],
        "slack_channel": data["slack_channel"],
        "sentry_project": data["sentry_project"],
        "sonarqube_project": data["sonarqube_project"],
        "pagerduty_service": data["pagerduty_service"],
        "tags": data["tags"],
    }

    service, _ = Service.objects.update_or_create(
        owner=data["owner"], name=data["name"], defaults=service_defaults
    )

    # Delete all environments as yaml file has precedence
    Environment.objects.filter(service=service).delete()

    # Add all environments
    for env in data["environments"]:
        e = Environment(service=service, name=env["name"])
        e.dashboard_url = env["dashboard_url"]
        e.service_urls = env["service_urls"]
        e.health_check_url = env["health_check_url"]
        e.save()


def get_zoo_file_content(proj: Dict) -> str:
    provider = get_scm_module(proj["provider"])
    return provider.get_file_content(
        proj["id"], settings.ZOO_YAML_FILE, settings.ZOO_YAML_DEFAULT_REF
    )
