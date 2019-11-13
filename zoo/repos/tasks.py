import hashlib
import itertools
import tempfile

from celery import shared_task
from django.conf import settings
import structlog

from ..analytics.tasks import repo_analyzers
from ..auditing import runner
from ..auditing.check_discovery import CHECKS as AUDITING_CHECKS
from .exceptions import MissingFilesError, RepositoryNotFoundError
from .github import get_repositories as get_github_repositories
from .gitlab import get_repositories as get_gitlab_repositories
from .models import Repository
from .utils import download_repository

log = structlog.get_logger()


@shared_task
def sync_repos():
    for project in itertools.chain(
        get_github_repositories(), get_gitlab_repositories()
    ):
        if settings.SYNC_REPOS_SKIP_FORKS and project["is_fork"]:
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
