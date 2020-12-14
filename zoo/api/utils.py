from enum import Enum
from textwrap import dedent

from graphql_relay import from_global_id

from ..auditing.models import Issue


def grab(model, global_id: str):
    """Return a Django model from a base64 encoded ID."""
    _type, pk = from_global_id(global_id)

    if _type == Issue.__name__:
        return model.objects.get(pk=pk)
    raise TypeError(
        f"The given ID is of type '{_type}' but we're updating '{model.__name__}' model"
    )


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


def doc(cls) -> str:
    if not cls.__doc__:
        return ""

    return "\n".join(dedent(line) for line in cls.__doc__.splitlines() if line)
