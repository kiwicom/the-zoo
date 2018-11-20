from zoo.services.ratings import SentryRater
from zoo.services.models import SentryIssueCounts
import pytest


@pytest.mark.parametrize(
    "percent_of_limit, issues, grade",
    [
        (0.90, SentryIssueCounts(-1, -1, -1, -1, -1), "F"),
        (0.89, SentryIssueCounts(-1, -1, -1, -1, -1), "E"),
        (0.50, SentryIssueCounts(-1, -1, -1, -1, -1), "E"),
        (0.49, SentryIssueCounts(-1, -1, -1, -1, -1), "D"),
        (0.10, SentryIssueCounts(-1, -1, -1, -1, -1), "D"),
        (0.09, SentryIssueCounts(-1, -1, -1, -1, 11), "C"),
        (0.09, SentryIssueCounts(101, -1, -1, -1, 9), "C"),
        (0.09, SentryIssueCounts(99, -1, 11, 4, 0), "B"),
        (0.09, SentryIssueCounts(99, -1, 9, 6, 0), "B"),
        (0.09, SentryIssueCounts(99, -1, 9, 4, 1), "B"),
        (0.09, SentryIssueCounts(99, -1, 9, 4, 0), "A"),
        (0.09, SentryIssueCounts(-1, 0, 0, 0, 0), "S"),
    ],
)
def test_sentry_rating(percent_of_limit, issues, grade):
    issue_count = int(SentryRater.RATE_LIMIT * percent_of_limit)
    sentry_rating = SentryRater(issue_count, issues).get_rating()
    assert sentry_rating["grade"] == grade
