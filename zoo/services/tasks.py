from datetime import datetime
import hashlib

from celery import shared_task
import dateutil.parser
from django.conf import settings
from django.utils import timezone
import requests
import structlog

from . import models

log = structlog.get_logger()


def fetch_sentry_project_issues(project_slug: str) -> dict:
    result = []
    api_request_url = "{0}/api/0/projects/{1}/{2}/issues/?statsPeriod=14d".format(
        settings.SENTRY_URL, settings.SENTRY_ORGANIZATION, project_slug
    )

    while api_request_url is not None:
        response = requests.get(
            api_request_url,
            headers={"Authorization": f"Bearer {settings.SENTRY_API_KEY}"},
        )

        response.raise_for_status()
        result.extend(response.json())

        next_link = response.links["next"]
        api_request_url = next_link["url"] if next_link["results"] == "true" else None

    return result


def update_or_create_issue(
    service: models.Service, sentry_issue_data: dict
) -> models.SentryIssue:
    try:
        sentry_issue = models.SentryIssue.objects.get(
            issue_id=sentry_issue_data["id"], service=service
        )
    except models.SentryIssue.DoesNotExist:
        sentry_issue = models.SentryIssue(
            title=sentry_issue_data["title"],
            culprit=sentry_issue_data["culprit"],
            short_id=sentry_issue_data["shortId"],
            issue_id=sentry_issue_data["id"],
            permalink=sentry_issue_data["permalink"],
            first_seen=dateutil.parser.parse(sentry_issue_data["firstSeen"]),
            service=service,
        )

    sentry_issue.events = sentry_issue_data["count"]
    sentry_issue.users = sentry_issue_data["userCount"]
    sentry_issue.last_seen = dateutil.parser.parse(sentry_issue_data["lastSeen"])

    if sentry_issue_data["assignedTo"]:
        sentry_issue.assignee = sentry_issue_data["assignedTo"]["name"]
    else:
        sentry_issue.assignee = None

    sentry_issue.full_clean()
    sentry_issue.save()

    return sentry_issue


def days_seen(count_per_day):
    return len([count for count in count_per_day if count > 0])


def classify_sentry_issue(sentry_issue: models.SentryIssue) -> str:
    count_per_day = [
        stat.count for stat in sentry_issue.stats.order_by("-timestamp")[:14]
    ]

    if days_seen(count_per_day[:14]) == 14:
        return models.SentryIssueCategory.STALE
    if days_seen(count_per_day[:14]) >= 7:
        return models.SentryIssueCategory.DECAYING
    if days_seen(count_per_day[:7]) >= 4:
        return models.SentryIssueCategory.SPOILED

    return models.SentryIssueCategory.FRESH


def cleanup_sentry_issues(service: models.Service) -> None:
    service.sentry_issues.all().delete()


@shared_task
def get_sentry_stats(service_id: int) -> None:
    try:
        service = models.Service.objects.get(id=service_id)
    except models.Service.DoesNotExist:
        log.info("get_sentry_stats.service_not_found", service_id=service_id)
        return

    if not service.sentry_project:
        return

    cleanup_sentry_issues(service)

    try:
        sentry_data = fetch_sentry_project_issues(service.sentry_project)
    except requests.RequestException:
        log.exception(
            "services.tasks.get_sentry_stats",
            service=service,
            sentry_project=service.sentry_project,
        )
        return

    for issue_data in sentry_data:
        sentry_issue = update_or_create_issue(service, issue_data)

        for stat in issue_data["stats"]["14d"]:
            timestamp = datetime.fromtimestamp(stat[0], timezone.now().tzinfo)
            models.SentryIssueStats.objects.update_or_create(
                issue=sentry_issue, timestamp=timestamp, defaults={"count": stat[1]}
            )

        sentry_issue.category = classify_sentry_issue(sentry_issue).value
        sentry_issue.full_clean()
        sentry_issue.save()

    service.update_rating()


@shared_task
def schedule_sentry_sync():
    for service in models.Service.objects.exclude(sentry_project=None):
        pk_hash = hashlib.sha256(f"sentry-{service.sentry_project}".encode())
        delay_s = int(pk_hash.hexdigest(), 16) % (60 * 60)

        get_sentry_stats.apply_async(
            args=(service.id,), countdown=delay_s, expires=delay_s + (60 * 60)
        )
