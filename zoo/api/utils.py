from enum import Enum

from ..auditing.models import Issue


class CheckResultStatus(Enum):
    KNOWN = "known"
    NEW = "new"
    FIXED = "fixed"
    WONTFIX = "wontfix"
    NOT_FOUND = "not found"
    REOPENED = "reopened"


found_result_status_mapping = {
    Issue.Status.NOT_FOUND: CheckResultStatus.NEW,
    Issue.Status.NEW: CheckResultStatus.KNOWN,
    Issue.Status.FIXED: CheckResultStatus.REOPENED,
    Issue.Status.REOPENED: CheckResultStatus.KNOWN,
    Issue.Status.WONTFIX: CheckResultStatus.WONTFIX,
}


not_found_result_status_mapping = {
    Issue.Status.NOT_FOUND: CheckResultStatus.NOT_FOUND,
    Issue.Status.NEW: CheckResultStatus.FIXED,
    Issue.Status.FIXED: CheckResultStatus.NOT_FOUND,
    Issue.Status.REOPENED: CheckResultStatus.FIXED,
    Issue.Status.WONTFIX: CheckResultStatus.FIXED,
}


def determine_check_result_status(is_found, issue_status):
    if is_found:
        return found_result_status_mapping[issue_status]
    return not_found_result_status_mapping[issue_status]
