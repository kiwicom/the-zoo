from celery import shared_task

from .models import Issue
from .utils import create_git_issue


@shared_task
def bulk_create_git_issues(issues):
    for issue_id, user_name, reverse_url in issues:
        issue = Issue.objects.get(id=issue_id)
        create_git_issue(issue, user_name, reverse_url)
