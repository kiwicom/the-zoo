from unittest.mock import patch

import arrow
import pytest
from django.utils import timezone
from faker import Faker

from zoo.services.models import (
    SentryIssue,
    SentryIssueCategory,
    SentryIssueStats,
    Service,
)
from zoo.services.tasks import get_sentry_stats

pytestmark = pytest.mark.django_db
fake = Faker()


class FakeSentryAPIResponse:
    def __init__(self, iid, stats):
        self.iid = iid
        self.issue_stats = self._build_issue_stats(stats)

    def _build_issue_stats(self, stats):
        base_timestamp = arrow.get(timezone.now())
        return [
            [
                base_timestamp.shift(days=-i).timestamp,
                fake.pyint() if stats is None else stats[i],
            ]
            for i in range(14)
        ]

    def get_response(self):
        return {
            "id": str(self.iid) if self.iid is not None else str(fake.pyint()),
            "shortId": f"{fake.word()}-{fake.pyint()}",
            "title": fake.sentence(),
            "culprit": fake.word(),
            "assignedTo": {
                "type": "user",
                "email": fake.email(),
                "name": fake.name(),
                "id": str(fake.pyint()),
            },
            "permalink": fake.url(),
            "count": sum(stat[1] for stat in self.issue_stats),
            "userCount": fake.pyint(),
            "firstSeen": fake.iso8601() + "Z",
            "lastSeen": fake.iso8601() + "Z",
            "stats": {"14d": self.issue_stats},
        }


def generate_sentry_api_response(iid=None, stats=None, **kwargs):
    return [FakeSentryAPIResponse(iid, stats).get_response()]


def test_sentry_stats__not_configured(service):
    get_sentry_stats(service.id)
    assert not SentryIssue.objects.filter(service=service).exists()


def test_sentry_stats__no_issues(mocker, service):
    sentry_api_response = []
    m_response = mocker.patch(
        "zoo.services.tasks.fetch_sentry_project_issues",
        return_value=sentry_api_response,
    )

    service.sentry_project = fake.word()
    service.full_clean()
    service.save()

    get_sentry_stats(service.id)
    m_response.assert_called_once()

    assert not SentryIssue.objects.filter(service=service).exists()


def test_sentry_stats__single_issue(mocker, service):
    sentry_api_response = generate_sentry_api_response()
    m_response = mocker.patch(
        "zoo.services.tasks.fetch_sentry_project_issues",
        return_value=sentry_api_response,
    )

    service.sentry_project = fake.word()
    service.full_clean()
    service.save()

    get_sentry_stats(service.id)
    assert m_response.call_count == 1

    assert SentryIssue.objects.all().count() == 1

    sentry_issue = SentryIssue.objects.get(service=service)
    api_data = sentry_api_response[0]

    assert sentry_issue.issue_id == int(api_data["id"])
    assert sentry_issue.short_id == api_data["shortId"]
    assert sentry_issue.title == api_data["title"]
    assert sentry_issue.culprit == api_data["culprit"]
    assert sentry_issue.assignee == api_data["assignedTo"]["name"]
    assert sentry_issue.permalink == api_data["permalink"]
    assert sentry_issue.events == int(api_data["count"])
    assert sentry_issue.users == int(api_data["userCount"])
    assert sentry_issue.first_seen == arrow.get(api_data["firstSeen"]).datetime
    assert sentry_issue.last_seen == arrow.get(api_data["lastSeen"]).datetime

    issue_stat = sentry_issue.stats.order_by("-timestamp").first()
    initial_value = issue_stat.count

    issue_stat.count += 1
    issue_stat.full_clean()
    issue_stat.save()

    assert issue_stat.count != initial_value

    service.sentry_project = fake.word()
    service.full_clean()
    service.save()

    get_sentry_stats(service.id)
    assert m_response.call_count == 2

    assert SentryIssue.objects.all().count() == 1
    sentry_issue = SentryIssue.objects.get(service=service)
    issue_stat = sentry_issue.stats.order_by("-timestamp").first()
    assert issue_stat.count == initial_value


@pytest.mark.parametrize(
    "stats, category",
    [
        ([0] * 14, SentryIssueCategory.FRESH),
        ([1000] + [0] * 13, SentryIssueCategory.FRESH),
        ([1000] * 4 + [0] * 10, SentryIssueCategory.SPOILED),
        ([1000] + [0] + [1000] * 12, SentryIssueCategory.DECAYING),
        ([1000] * 4 + [0] + [1000] * 9, SentryIssueCategory.DECAYING),
        ([1000] * 7 + [0] * 7, SentryIssueCategory.DECAYING),
        ([1000] * 7 + [0] + [1000] * 6, SentryIssueCategory.DECAYING),
        ([1000] * 14, SentryIssueCategory.STALE),
    ],
)
def test_sentry_stats__issue_stats(stats, category, mocker, service):
    sentry_api_response = generate_sentry_api_response(iid=None, stats=stats)
    m_response = mocker.patch(
        "zoo.services.tasks.fetch_sentry_project_issues",
        return_value=sentry_api_response,
    )

    service.sentry_project = fake.word()
    service.full_clean()
    service.save()

    get_sentry_stats(service.id)
    m_response.assert_called_once()

    assert SentryIssue.objects.filter(service=service).count() == 1

    sentry_issue = SentryIssue.objects.get(service=service)
    assert SentryIssueStats.objects.filter(issue=sentry_issue).count() == 14
    assert sentry_issue.events == sum(stats)
    assert sentry_issue.category == category.value
