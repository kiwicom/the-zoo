import structlog
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_GET
from django.views.generic import ListView

from . import models
from .exceptions import RepositoryNotFoundError
from .models import Provider, Repository
from .utils import get_scm_module

log = structlog.get_logger()


class RepoList(ListView):
    model = models.Repository


def repo_details(request, provider, repo_id):
    scm_module = get_scm_module(provider)

    try:
        details = scm_module.get_project_details(repo_id)
    except RepositoryNotFoundError:
        raise Http404(f"Project {repo_id} not found")

    return JsonResponse(details)


@require_GET
def get_gitlab_envs(request):
    project_id = request.GET.get("project_id")

    if not project_id:
        return JsonResponse({"message": "Missing project_id"}, safe=False)
    project_id = 1
    try:
        repo = Repository.objects.get(id=project_id, provider=Provider.GITLAB.value)
    except RepositoryNotFoundError:
        return JsonResponse({"message": "Wrong project_id"}, safe=False)

    parsed_envs = [{
                "name": gl_env.name,
                "dashboardUrl": gl_env.external_url,
                "logsUrl": "",
                "serviceUrl": [],
                "openapiUrl": "",
            } for gl_env in repo.repository_environments.all()]
    return JsonResponse(parsed_envs, safe=False)
