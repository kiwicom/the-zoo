import tempfile

import graphene
from django.core.exceptions import PermissionDenied

from ..auditing.check_discovery import CHECKS
from ..auditing.models import Issue
from ..auditing.runner import check_repository
from ..auditing.utils import create_git_issue
from ..repos.models import Repository
from ..repos.utils import download_repository
from . import types
from .utils import CheckResultStatus, determine_check_result_status, doc, grab


class SetWontfix(graphene.relay.ClientIDMutation):
    class Input:
        issue_id = graphene.String(required=True)
        comment = graphene.String()

    issue = graphene.Field(types.Issue)

    @classmethod
    def mutate_and_get_payload(cls, root, info, *, issue_id, comment=None):
        issue = grab(Issue, issue_id)
        issue.set_wontfix(comment=comment)
        return SetWontfix(issue=issue)


class OpenIssue(graphene.relay.ClientIDMutation):
    class Input:
        issue_id = graphene.String(required=True)
        page_url = graphene.String(required=True)

    issue = graphene.Field(types.Issue)

    @classmethod
    def mutate_and_get_payload(cls, root, info, *, issue_id, page_url):
        issue = grab(Issue, issue_id)
        create_git_issue(
            issue, user_name=info.context.user.username, reverse_url=page_url
        )
        issue.refresh_from_db()
        return OpenIssue(issue=issue)


class ApplyPatches(graphene.relay.ClientIDMutation):
    class Input:
        issue_id = graphene.String(required=True)

    issue = graphene.Field(types.Issue)

    @classmethod
    def mutate_and_get_payload(cls, root, info, *, issue_id):
        issue = grab(Issue, issue_id)
        success = issue.handle_patches()
        if not success:
            raise PermissionDenied("Could not apply patches: Forbidden.")
        return ApplyPatches(issue=issue)


class CheckRepositoryByCommit(graphene.relay.ClientIDMutation):
    """Runs checks on repository on the fly and returns found issues.

    Statuses of results are determined from comparison with Repository's known
    issues on master branch.
    """

    class Input:
        owner = graphene.String(required=True)
        name = graphene.String(required=True)
        sha = graphene.String(required=True)
        only_found = graphene.Boolean(
            default_value=False,
            description="Return only found issues (exclude fixed or not found).",
        )

    all_check_results = graphene.List(types.CheckResult)
    repository = graphene.Field(types.Repository)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            repository = Repository.objects.get(
                owner=input["owner"], name=input["name"]
            )
        except Repository.DoesNotExist:
            raise Exception("{owner}/{name} is not known to the Zoo.".format(**input))

        known_issues = dict(repository.issues.values_list("kind_key", "status"))

        with tempfile.TemporaryDirectory() as repo_dir:
            repo_path = download_repository(repository, repo_dir, sha=input["sha"])
            results = list(check_repository(CHECKS, repository, repo_path))

        check_results = []
        for result in results:
            if input["only_found"] and not result.is_found:
                continue

            if result.issue_key in known_issues:
                issue_status = Issue.Status(known_issues[result.issue_key])
                status = determine_check_result_status(result.is_found, issue_status)
            else:
                if result.is_found:
                    status = CheckResultStatus.NEW
                else:
                    status = CheckResultStatus.NOT_FOUND

            check_results.append(
                types.CheckResult(
                    is_found=result.is_found,
                    kind_key=result.issue_key,
                    status=status,
                    details=result.details,
                )
            )

        return CheckRepositoryByCommit(
            all_check_results=check_results,
            repository=types.Repository.from_db(repository),
        )


class Mutation:
    check_repository_by_commit = CheckRepositoryByCommit.Field(
        description=doc(CheckRepositoryByCommit)
    )
    set_wontfix = SetWontfix.Field(description=doc(SetWontfix))
    open_issue = OpenIssue.Field(description=doc(OpenIssue))
    apply_patches = ApplyPatches.Field(description=doc(ApplyPatches))
