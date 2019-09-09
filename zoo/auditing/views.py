from collections import defaultdict, OrderedDict
import itertools
import json
import tempfile

from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from . import models, runner, tasks
from ..libraries.models import Library
from ..repos.tasks import pull
from ..repos.utils import download_repository
from ..services.models import Service
from .check_discovery import KINDS
from .utils import create_git_issue, PatchHandler


class AuditOverview(TemplateView):
    template_name = "audit_overview.html"

    @staticmethod
    def get_available_namespaces():
        return {
            kind.namespace for kind in KINDS.values() if kind.namespace != "deleted"
        }

    @staticmethod
    def get_available_owners():
        return {
            project.owner
            for project in itertools.chain(Service.objects.all(), Library.objects.all())
        }

    @staticmethod
    def get_available_status():
        return {
            project.status
            for project in itertools.chain(Service.objects.all(), Library.objects.all())
            if project.status is not None
        }

    @classmethod
    def get_available_filters(cls):
        return [
            *({"name": s, "type": "owner"} for s in cls.get_available_owners()),
            *({"name": n, "type": "namespace"} for n in cls.get_available_namespaces()),
            *({"name": n, "type": "status"} for n in cls.get_available_status()),
        ]

    @classmethod
    def get_projects(cls, model, owner_filters, status_filters):
        project_list = model.objects.exclude(repository_id=None).select_related(
            "repository"
        )

        if owner_filters:
            project_list = project_list.filter(owner__in=owner_filters)

        if status_filters:
            project_list = project_list.filter(status__in=status_filters)

        return project_list

    @classmethod
    def get_services(cls, *args):
        return cls.get_projects(Service, *args)

    @classmethod
    def get_libraries(cls, *args):
        return cls.get_projects(Library, *args)

    @classmethod
    def _get_repos_by_issue(cls, repository_ids):
        issues = (
            models.Issue.objects.filter(
                status__in=[
                    models.Issue.Status.NEW.value,
                    models.Issue.Status.REOPENED.value,
                ],
                kind_key__in=KINDS,
                repository_id__in=repository_ids,
            )
            .values("kind_key", "repository_id")
            .all()
        )
        repos_by_issue = defaultdict(set)
        for issue in issues:
            repos_by_issue[issue["kind_key"]].add(issue["repository_id"])

        return repos_by_issue

    @classmethod
    def _get_projects_by_repo(cls, *args):
        projects = itertools.chain(cls.get_services(*args), cls.get_libraries(*args))
        projects_by_repo = defaultdict(list)

        for project in projects:
            projects_by_repo[project.repository_id].append(
                {
                    "id": project.id,
                    "name": project.name,
                    "owner": project.owner,
                    "url": project.get_absolute_url(),
                    "type": project.__class__.__name__.lower(),
                    "repository": {
                        "id": project.repository_id,
                        "url": project.repository.url,
                        "owner": project.repository.owner,
                        "name": project.repository.name,
                    },
                }
            )
        return projects_by_repo

    @classmethod
    def get_issues(cls, owner_filters, namespace_filters, status_filters):
        kinds = defaultdict(lambda: {"count": 0, "projects": []})

        if not namespace_filters:
            namespace_filters = cls.get_available_namespaces()

        projects_by_repo = cls._get_projects_by_repo(owner_filters, status_filters)
        repos_by_issue = cls._get_repos_by_issue(projects_by_repo)

        for kind_key, repos in repos_by_issue.items():
            kind = KINDS[kind_key]
            if kind.namespace not in namespace_filters:
                continue

            kinds[kind.key]["title"] = kind.title
            kinds[kind.key]["description"] = kind.description
            kinds[kind.key]["effort"] = kind.effort.value
            kinds[kind.key]["severity"] = kind.severity.value
            kinds[kind.key]["patch"] = kind.patch

            for repo_id in repos:
                if repo_id in projects_by_repo:
                    kinds[kind.key]["projects"] += projects_by_repo[repo_id]

            kinds[kind.key]["projects"].sort(key=lambda d: d["name"])
            kinds[kind.key]["count"] = len(kinds[kind.key]["projects"])

        return OrderedDict(sorted(kinds.items()))

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            owner_filters = self.request.GET.getlist("owner")
            namespace_filters = self.request.GET.getlist("namespace")
            status_filters = self.request.GET.getlist("status")

            return JsonResponse(
                {
                    "issues": self.get_issues(
                        owner_filters, namespace_filters, status_filters
                    ),
                    "filters": self.get_available_filters(),
                    "applied_filters": [
                        *({"name": s, "type": "owner"} for s in owner_filters),
                        *({"name": n, "type": "namespace"} for n in namespace_filters),
                        *({"name": n, "type": "status"} for n in status_filters),
                    ],
                }
            )

        return self.render_to_response(self.get_context_data(**kwargs))


class AuditReport(TemplateView):
    template_name = "audit_report.html"
    models = {"services": Service, "libraries": Library}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        project = context["project"]

        if "force" in self.request.GET and project.repository:
            pull(project.repository.remote_id, project.repository.provider)
            return redirect(
                "audit_report",
                self.kwargs["project_type"],
                self.kwargs["owner_slug"],
                self.kwargs["name_slug"],
            )

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_cls = self.models.get(self.kwargs["project_type"])

        if project_cls is None:
            raise Http404("Project.DoesNotExist")

        try:
            project = (
                project_cls.objects.select_related("repository")
                .prefetch_related("repository__issues")
                .get(
                    owner_slug=self.kwargs["owner_slug"],
                    name_slug=self.kwargs["name_slug"],
                )
            )
        except project_cls.DoesNotExist:
            raise Http404(f"{project_cls.__name__}.DoesNotExist")

        context["project"] = project
        context["project_type"] = self.kwargs["project_type"]
        context["issues"] = defaultdict(list)

        if project.repository:
            for issue in project.repository.issues.filter(deleted=False).exclude(
                status__in=[
                    models.Issue.Status.FIXED.value,
                    models.Issue.Status.NOT_FOUND.value,
                    models.Issue.Status.WONTFIX.value,
                ]
            ):
                context["issues"][issue.kind.category].append(issue)

        # with defaultdict {{ issues.items }} would be empty, and we want consistent issue order anyway
        context["issues"] = OrderedDict(
            (key, sorted(value, key=lambda x: x.kind_key))
            for key, value in sorted(context["issues"].items())
        )

        deleted_issues = project.repository.issues.filter(deleted=True).all()
        if deleted_issues:
            unknown_ctg = "Deprecated Issues"
            context["issues"][unknown_ctg] = deleted_issues

        return context


class IssuePatch(TemplateView):
    template_name = "issue_patch.html"

    def get(self, request, *args, **kwargs):
        issue = models.Issue.objects.get(pk=self.kwargs["issue_pk"])
        repository = issue.repository

        with tempfile.TemporaryDirectory() as repo_dir:
            repo_path = download_repository(repository, repo_dir)
            context = runner.CheckContext(repository, repo_path)

            handler = PatchHandler(issue)
            patches = handler.run_patches(context)

        patches_key = handler.save_patches()
        context = {"patches": patches, "patches_key": patches_key}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        issue = models.Issue.objects.get(pk=self.kwargs["issue_pk"])
        handler = PatchHandler(issue)

        if not handler.handle_patches(request):
            return HttpResponseForbidden()

        return redirect(
            "audit_report",
            self.kwargs["project_type"],
            self.kwargs["owner_slug"],
            self.kwargs["name_slug"],
        )


@require_POST
def open_bulk_git_issues(request):
    data = json.loads(request.body)

    issues = []
    for kind_key, repositories in data["selectedIssues"].items():
        issues += models.Issue.objects.filter(
            status__in=[
                models.Issue.Status.NEW.value,
                models.Issue.Status.REOPENED.value,
            ],
            repository_id__in=repositories,
            kind_key=kind_key,
            remote_issue_id__isnull=True,
        ).all()

    user_name = request.user.get_username()
    redirect_uri = request.build_absolute_uri(
        reverse("audit_overview")
        if "owner" not in data
        else reverse("owned_audit_overview", args=[data["owner"]])
    )
    new_issues = [(issue.id, user_name, redirect_uri) for issue in issues]
    tasks.bulk_create_git_issues.delay(new_issues)

    return JsonResponse(data)


@require_POST
def apply_bulk_patches(request):
    data = json.loads(request.body)

    issues = []
    for kind_key, repositories in data["selectedIssues"].items():
        issues += models.Issue.objects.filter(
            status__in=[
                models.Issue.Status.NEW.value,
                models.Issue.Status.REOPENED.value,
            ],
            repository_id__in=repositories,
            kind_key=kind_key,
            merge_request_id__isnull=True,
        ).all()

    patching_issues = [issue.id for issue in issues]
    tasks.bulk_apply_patches.delay(patching_issues)

    return JsonResponse(data)


@require_POST
def open_git_issue(request, project_type, owner_slug, name_slug, issue_pk):
    issue = models.Issue.objects.get(pk=issue_pk)

    create_git_issue(
        issue,
        request.user.get_username(),
        request.build_absolute_uri(
            reverse("audit_report", args=[project_type, owner_slug, name_slug])
        ),
    )

    return redirect("audit_report", project_type, owner_slug, name_slug)


@require_POST
def wontfix_issue(request, project_type, owner_slug, name_slug, issue_pk):
    issue = models.Issue.objects.get(pk=issue_pk)

    issue.status = issue.Status.WONTFIX.value
    issue.comment = request.POST["comment"]
    issue.full_clean()
    issue.save()

    return redirect("audit_report", project_type, owner_slug, name_slug)
