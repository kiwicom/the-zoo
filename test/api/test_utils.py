import pytest

from zoo.auditing.models import Issue

from zoo.api import utils as uut


@pytest.mark.parametrize(
    "is_found, issue_status, result_status",
    (
        (True, Issue.Status.NOT_FOUND, uut.CheckResultStatus.NEW),
        (True, Issue.Status.NEW, uut.CheckResultStatus.KNOWN),
        (True, Issue.Status.FIXED, uut.CheckResultStatus.REOPENED),
        (True, Issue.Status.REOPENED, uut.CheckResultStatus.KNOWN),
        (True, Issue.Status.WONTFIX, uut.CheckResultStatus.WONTFIX),
        (False, Issue.Status.NOT_FOUND, uut.CheckResultStatus.NOT_FOUND),
        (False, Issue.Status.NEW, uut.CheckResultStatus.FIXED),
        (False, Issue.Status.REOPENED, uut.CheckResultStatus.FIXED),
        (False, Issue.Status.FIXED, uut.CheckResultStatus.NOT_FOUND),
        (False, Issue.Status.WONTFIX, uut.CheckResultStatus.FIXED),
    ),
)
def test_determine_check_result_status(is_found, issue_status, result_status):
    assert uut.determine_check_result_status(is_found, issue_status) == result_status
