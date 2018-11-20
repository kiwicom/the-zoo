from django.http import Http404, JsonResponse
from django.views.generic import ListView
import structlog

from . import models
from .exceptions import RepositoryNotFoundError
from .utils import get_scm_module

log = structlog.get_logger()


class RepoList(ListView):
    model = models.Repository


def repo_details(request, provider, repo_id):

    if repo_id is None:
        return JsonResponse({"error": "repository id not specified"}, status=400)
    if provider is None:
        return JsonResponse({"error": "provider is not specified"}, status=400)

    scm_module = get_scm_module(provider)

    try:
        details = scm_module.get_project_details(repo_id)
    except RepositoryNotFoundError:
        raise Http404(f"Project {repo_id} not found")
    return JsonResponse(details)
