from collections import defaultdict, OrderedDict
import json
import pathlib
import tempfile

from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from . import models, runner, tasks
from ..base import redis
from ..repos.tasks import pull
from ..repos.utils import download_repository
from ..services.models import Service
from .utils import create_git_issue, get_md5_hash


class AuditOverview(TemplateView):
    template_name = "audit_overview.html"

    @staticmethod
    def get_available_namespaces():
        return {i.kind.namespace for i in models.Issue.objects.all()}

    @staticmethod
    def get_available_owners():
        return {s.owner for s in Service.objects.all()}

    @staticmethod
    def get_available_status():
        return {s.status for s in Service.objects.all() if s.status is not None}

    @classmethod
    def get_available_filters(cls):
        return [
            *({"name": s, "type": "owner"} for s in cls.get_available_owners()),
            *({"name": n, "type": "namespace"} for n in cls.get_available_namespaces()),
            *({"name": n, "type": "status"} for n in cls.get_available_status()),
        ]

    @staticmethod
    def get_services(owner_filters, status_filters):
        service_list = (
            Service.objects.exclude(repository_id=None)
            .select_related("repository")
            .prefetch_related("repository__issues")
        )

        if owner_filters:
            service_list = service_list.filter(owner__in=owner_filters)

        if status_filters:
            service_list = service_list.filter(status__in=status_filters)

        return service_list

    @classmethod
    def get_issues(cls, owner_filters, namespace_filters, status_filters):
        kinds = defaultdict(lambda: {"services": []})

        if not namespace_filters:
            namespace_filters = cls.get_available_namespaces()

        for service in cls.get_services(owner_filters, status_filters):
            for issue in service.repository.issues.all():
                if issue.kind.namespace not in namespace_filters:
                    continue

                kinds[issue.kind_key]["title"] = issue.kind.title
                kinds[issue.kind_key]["description"] = issue.kind.description
                kinds[issue.kind_key]["effort"] = issue.kind.effort.value
                kinds[issue.kind_key]["severity"] = issue.kind.severity.value
                kinds[issue.kind_key]["services"].append(
                    {
                        "id": service.id,
                        "pk": issue.pk,
                        "url": issue.remote_issue_url,
                        "status": issue.status,
                        "kind_key": issue.kind_key,
                        "remote_id": issue.remote_issue_id
                        if issue.remote_issue_id is not None
                        else None,
                    }
                )

        return OrderedDict(sorted(kinds.items()))

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            owner_filters = self.request.GET.getlist("service_owner")
            namespace_filters = self.request.GET.getlist("namespace")
            status_filters = self.request.GET.getlist("status")

            return JsonResponse(
                {
                    "services": [
                        {"id": s.id, "name": s.name, "owner": s.owner}
                        for s in self.get_services(owner_filters, status_filters)
                    ],
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

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        service = context["service"]

        if "force" in self.request.GET and service.repository:
            pull(service.repository.remote_id, service.repository.provider)
            return redirect(
                "audit_report",
                self.kwargs["service_owner_slug"],
                self.kwargs["service_name_slug"],
            )

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            service = (
                Service.objects.select_related("repository")
                .prefetch_related("repository__issues")
                .get(
                    owner_slug=self.kwargs["service_owner_slug"],
                    name_slug=self.kwargs["service_name_slug"],
                )
            )
        except Service.DoesNotExist:
            raise Http404("Service.DoesNotExist")

        context["service"] = service
        context["issues"] = defaultdict(list)

        if service.repository:
            for issue in service.repository.issues.filter(deleted=False).exclude(
                status__in=[
                    models.Issue.Status.FIXED.value,
                    models.Issue.Status.NOT_FOUND.value,
                ]
            ):
                context["issues"][issue.kind.category].append(issue)

        # with defaultdict {{ issues.items }} would be empty, and we want consistent issue order anyway
        context["issues"] = OrderedDict(
            (key, sorted(value, key=lambda x: x.kind_key))
            for key, value in sorted(context["issues"].items())
        )

        deleted_issues = service.repository.issues.filter(deleted=True).all()
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
            patches, actions = self.get_patch_data(issue, repo_path)

        self.store_actions_hash(issue, actions)
        context = {"patches": patches, "actions": actions}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        issue = models.Issue.objects.get(pk=self.kwargs["issue_pk"])
        repository = issue.repository

        actions_field = request.POST.get("actions", "[]")
        is_valid = self.validate_actions_hash(issue, actions_field)

        if not is_valid:
            return HttpResponseForbidden()

        actions = json.loads(actions_field)
        branch_name = f"zoo/{issue.kind.id}"

        repository.scm_module.create_remote_commit(
            repository.remote_id,
            actions=actions,
            message=issue.kind.title,
            branch=branch_name,
        )
        issue.merge_request_id = repository.scm_module.create_merge_request(
            repository.remote_id,
            title=issue.kind.title,
            description=issue.description_md,
            source_branch=branch_name,
            reverse_url=request.build_absolute_uri(reverse("audit_overview")),
        )
        issue.save()

        return redirect(
            "audit_report",
            self.kwargs["service_owner_slug"],
            self.kwargs["service_name_slug"],
        )

    def get_patch_data(self, issue, repo_path):
        context = runner.CheckContext(issue.repository, repo_path)

        patches, actions = [], []
        for patch in issue.kind.apply_patch(context):
            file_path = pathlib.Path(patch.file_path)
            previous_path = (
                pathlib.Path(patch.previous_path)
                if patch.previous_path is not None
                else None
            )
            repo_path_offset = len(repo_path.as_posix()) + 1

            data = {}
            data["action"] = patch.action
            data["file_path"] = file_path.as_posix()[repo_path_offset:]

            if patch.action in ["update", "delete"]:
                data["previous_content"] = file_path.read_text()

            if patch.action in ["create", "update"]:
                data["content"] = patch.content

            if previous_path is not None and previous_path != file_path:
                data["previous_path"] = previous_path.as_posix()[repo_path_offset:]

            patches.append(data)
            actions.append(dict(data))
            actions[-1].pop("previous_path", None)

        return patches, json.dumps(actions)

    def get_cache_key(self, issue):
        return f"_cache.issues.{issue.id}"

    def store_actions_hash(self, issue, actions):
        md5_hash = get_md5_hash(actions.encode("utf-8"))
        redis_conn = redis.get_connection()

        key = self.get_cache_key(issue)
        redis_conn.set(key, md5_hash, ex=600)
        return md5_hash

    def validate_actions_hash(self, issue, actions):
        md5_hash = get_md5_hash(actions.encode("utf-8"))
        redis_conn = redis.get_connection()

        value = redis_conn.get(self.get_cache_key(issue))
        return value is not None and value.decode("utf-8") == md5_hash


@require_POST
def open_bulk_git_issues(request):
    data = json.loads(request.body)

    user_name = request.user.get_username()
    redirect_uri = request.build_absolute_uri(
        reverse("audit_overview")
        if "owner" not in data
        else reverse("owned_audit_overview", args=[data["owner"]])
    )
    issues = [(pk, user_name, redirect_uri) for pk in data["pk_list"]]
    tasks.bulk_create_git_issues.delay(issues)

    owner_filters = {
        f["name"] for f in data["filters"]["applied"] if f["type"] == "owner"
    }
    namespace_filters = {
        f["name"] for f in data["filters"]["applied"] if f["type"] == "namespace"
    }
    status_filters = {
        f["name"] for f in data["filters"]["applied"] if f["type"] == "status"
    }

    return JsonResponse(
        {
            "services": [
                {"id": s.id, "name": s.name, "owner": s.owner}
                for s in AuditOverview.get_services(owner_filters, status_filters)
            ],
            "issues": AuditOverview.get_issues(
                owner_filters, namespace_filters, status_filters
            ),
            "filters": data["filters"],
        }
    )


@require_POST
def open_git_issue(request, service_owner_slug, service_name_slug, issue_pk):
    issue = models.Issue.objects.get(pk=issue_pk)

    create_git_issue(
        issue,
        request.user.get_username(),
        request.build_absolute_uri(
            reverse("audit_report", args=[service_owner_slug, service_name_slug])
        ),
    )

    return redirect("audit_report", service_owner_slug, service_name_slug)


@require_POST
def wontfix_issue(request, service_owner_slug, service_name_slug, issue_pk):
    issue = models.Issue.objects.get(pk=issue_pk)

    issue.status = issue.Status.WONTFIX.value
    issue.comment = request.POST["comment"]
    issue.full_clean()
    issue.save()

    return redirect("audit_report", service_owner_slug, service_name_slug)
