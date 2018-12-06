from celery import shared_task
from django.db.models import Count

from .models import Issue, IssueCountByKindSnapshot, IssueCountByRepositorySnapshot
from .utils import create_git_issue


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
