from collections import defaultdict
from datetime import timedelta
from typing import Dict, List

from django.db import models
from django.db.models import Q, Sum
from django.utils import timezone

from .models import SentryIssueCategory


class SentryIssueQuerySet(models.QuerySet):
    def calculate_weekly_sentry_stats(self) -> Dict[str, int]:
        one_week_ago = timezone.now().date() - timedelta(days=7)
        last_week_issues = self.filter(last_seen__gte=one_week_ago).annotate(
            freq=Sum("stats__count", filter=Q(stats__timestamp__gte=one_week_ago))
        )
        weekly_events = last_week_issues.aggregate(Sum("freq"))["freq__sum"] or 0
        weekly_users = last_week_issues.aggregate(Sum("users"))["users__sum"] or 0

        return {"events": weekly_events, "users": weekly_users}

    def problematic(self) -> list:
        """Problematic issues sorted by category and last time seen."""
        ISSUE_ORDER = {
            SentryIssueCategory.STALE.value: 0,
            SentryIssueCategory.DECAYING.value: 1,
            SentryIssueCategory.SPOILED.value: 2,
        }

        return sorted(
            self.filter(category__in=ISSUE_ORDER.keys()).all(),
            key=lambda k: (ISSUE_ORDER[k.category], k.last_seen),
        )

    def generate_sentry_histogram(self) -> Dict[int, List[int]]:
        result = defaultdict(list)

        def bar_height(day, max_events_count):
            if not all([day.count, max_events_count]):
                return 0
            return max(day.count / max_events_count, 0.175)

        for issue in self:
            last_two_weeks = sorted(issue.stats.all(), key=lambda x: x.timestamp)[:14]
            max_events_count = max(day.count for day in last_two_weeks)

            for day in last_two_weeks:
                result[issue.id].append(
                    {
                        "value": bar_height(day, max_events_count),
                        "tooltip": f"""
                            <h4>{day.timestamp.strftime('%d/%m/%Y')}</h4>
                            <strong>{day.count}</strong> events
                        """,
                    }
                )

        return dict(result)


SentryIssueManager = SentryIssueQuerySet.as_manager
