import arrow
from celery import shared_task
from django.conf import settings
from django.db.models import Count
import structlog

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
    days = settings.ZOO_AUDITING_DROP_ISSUES

    if not days:
        return

    x_days_ago = arrow.utcnow().shift(days=-days).datetime
    deleted_count, _ = Issue.objects.filter(
        last_check__lt=x_days_ago, deleted=True
    ).delete()

    log.info(
        "auditing.issues.deleted",
        deleted_issues_count=deleted_count,
        reason="expired_issues",
    )
