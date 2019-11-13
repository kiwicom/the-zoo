import json
import tempfile

from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, JsonResponse
from django.views.generic import ListView
from prance import ResolvingParser, ValidationError
from prance.util.url import ResolutionError
import structlog
from yaml.composer import ComposerError
from yaml.scanner import ScannerError

from . import models
from ..base import redis
from .exceptions import MissingFilesError, RepositoryNotFoundError
from .models import Repository
from .utils import download_repository, get_scm_module

log = structlog.get_logger()


OPENAPI_SCAN_EXCLUDE = ["k8s", "test", ".gitlab", ".github"]


class RepoList(ListView):
    model = models.Repository


def repo_details(request, provider, repo_id):
    scm_module = get_scm_module(provider)

    try:
        details = scm_module.get_project_details(repo_id)
    except RepositoryNotFoundError:
        raise Http404(f"Project {repo_id} not found")

    return JsonResponse(details)


def _parse_file(path, base=None):
    try:
        parser = ResolvingParser(str(path))
        return parser.specification
    except (
        ValidationError,
        ResolutionError,
        ComposerError,
        ScannerError,
        AttributeError,
    ) as err:
        log.info(
            "repos.views.openapi.invalid", path=str(path.relative_to(base)), error=err
        )


def openapi_definition(request, provider, repo_id):
    try:
        repository = Repository.objects.get(remote_id=repo_id, provider=provider)
    except Repository.DoesNotExist:
        return JsonResponse({"error": "repository not found"}, status=404)

    redis_conn = redis.get_connection()
    key = f"openapi-{provider}-{repo_id}"

    if redis_conn.exists(key) and "force" not in request.GET:
        return JsonResponse(json.loads(redis_conn.get(key)), safe=False)

    specs = []

    with tempfile.TemporaryDirectory() as repo_dir:
        try:
            repo_path = download_repository(repository, repo_dir)
        except (MissingFilesError, RepositoryNotFoundError) as err:
            log.info("repos.views.openapi.git_error", repo=repository, error=err)
            return JsonResponse({"error": "error downloading repository"}, status=500)

        for ext in ("json", "yml", "yaml"):
            for path in repo_path.glob(f"**/*.{ext}"):
                if any([directory in str(path) for directory in OPENAPI_SCAN_EXCLUDE]):
                    continue

                specs.append(_parse_file(path, repo_path))

    specs = list(filter(None, specs))

    redis_conn.set(key, json.dumps(specs, cls=DjangoJSONEncoder), ex=1800)
    return JsonResponse(specs, safe=False)
