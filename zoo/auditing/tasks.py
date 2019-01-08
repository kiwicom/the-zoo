import arrow
from celery import shared_task
from django.conf import settings
from django.db.models import Count
import structlog

from .check_discovery import KINDS
from .models import Issue, IssueCountByKindSnapshot, IssueCountByRepositorySnapshot
from .utils import create_git_issue

log = structlog.get_logger()


@shared_task
def bulk_create_git_issues(issues):
    for issue_id, user_name, reverse_url in issues:
        issue = Issue.objects.get(id=issue_id)
        create_git_issue(issue, user_name, reverse_url)


@shared_task
def take_issue_table_snapshots():
    issues = Issue.objects.all()
    for row in issues.values("repository_id", "status").annotate(count=Count("*")):
        snapshot = IssueCountByRepositorySnapshot(**row)
        snapshot.full_clean()
        snapshot.save()
    for row in issues.values("kind_key", "status").annotate(count=Count("*")):
        snapshot = IssueCountByKindSnapshot(**row)
        snapshot.full_clean()
        snapshot.save()


@shared_task
def cleanup_issues():
    deleted_count, _ = Issue.objects.exclude(kind_key__in=KINDS.keys()).delete()
    log.info(
        "auditing.issues.deleted",
        deleted_issues_count=deleted_count,
        reason="deleted_kinds",
    )

    hours = settings.ZOO_AUDITING_DROP_ISSUES

    if not hours:
        return

    x_hours_ago = arrow.utcnow().shift(hours=-hours).datetime
    recent_kinds = Issue.objects.filter(last_check__gt=x_hours_ago).values_list(
        "kind_key", flat=True
    )
    deleted_count, _ = Issue.objects.filter(
        last_check__lt=x_hours_ago, kind_key__in=recent_kinds
    ).delete()

    log.info(
        "auditing.issues.deleted",
        deleted_issues_count=deleted_count,
        reason="expired_issues",
    )
