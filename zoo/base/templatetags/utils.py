import re

from django import template
from django.conf import settings

from ...auditing.check_discovery import Effort, Severity
from ...objectives.models import Objective
from ...services.models import Impact, SentryIssueCategory, Status

register = template.Library()


known_icons = {
    "rating": {
        r"S": "trophy",
        r"A": "check circle",
        r"B": "info circle",
        r"C": "info circle",
        r"D": "exclamation circle",
        r"E": "exclamation circle",
        r"F": "times circle",
    },
    "analytics_health": {"True": "check", "False": "times", "None": "question"},
    "analytics_internal": {"True": "check", "False": "times"},
}

known_colors = {
    "status": {
        Status.BETA.value: "yellow",
        Status.DEPRECATED.value: "red",
        Status.DISCONTINUED.value: "grey",
        Status.PRODUCTION.value: "green",
    },
    "impact": {
        Impact.CUSTOMERS.value: "red",
        Impact.EMPLOYEES.value: "blue",
        Impact.PROFIT.value: "black",
    },
    "datacenter": {
        r"AWS*": "orange",
        r"Google*": "green",
        r"Hetzner*": "red",
        r"DigitalOcean*": "blue",
    },
    "rating": {
        r"S": "teal",
        r"A": "green",
        r"B": "yellow",
        r"C": "yellow",
        r"D": "orange",
        r"E": "orange",
        r"F": "red",
    },
    "sentry_issue_category": {
        SentryIssueCategory.SPOILED.value: "yellow",
        SentryIssueCategory.DECAYING.value: "orange",
        SentryIssueCategory.STALE.value: "red",
    },
    "issue_effort": {
        Effort.LOW.value: "green",
        Effort.MEDIUM.value: "orange",
        Effort.HIGH.value: "red",
    },
    "issue_severity": {
        Severity.ADVICE.value: "green",
        Severity.WARNING.value: "orange",
        Severity.CRITICAL.value: "red",
    },
    "analytics_health": {"True": "green", "False": "red", "None": "yellow"},
    "analytics_internal": {"True": "green", "False": "red"},
}


@register.inclusion_tag("services/service_link.html")
def service_link(name, url, icon=None):
    return {"name": name, "url": url, "icon": icon or name}


@register.simple_tag
def label_icon(category, name):
    name = str(name)
    if category in known_icons:
        for pattern in known_icons[category]:
            if re.match(pattern, name):
                return known_icons[category][pattern]
    return ""


@register.simple_tag
def label_color(category, name):
    name = str(name)
    if category in known_colors:
        for pattern in known_colors[category]:
            if re.match(pattern, name):
                return known_colors[category][pattern]

    return "brown"


@register.simple_tag
def settings_value(name):
    return getattr(settings, name)


@register.filter
def percent(value):
    return f"{value:.2%}"


@register.filter
def short_int_word(value: int) -> str:
    if isinstance(value, int):
        if value >= 1_000_000:
            return f"~{round(value/1000000, 1)}M"
        if value >= 1000:
            return f"~{round(value/1000, 1)}k"

    return f"{value}"


@register.filter
def times(value: int, multiplier: int) -> int:
    """Multiply the two arguments.

    This is meant to be used only to calculate styling values, never data.
    """
    return value * multiplier


@register.simple_tag
def objective_row_color(objective: Objective) -> str:
    if objective.latest_value:
        return "positive" if objective.meets_target else "negative"
    return ""


@register.simple_tag
def objective_label_color(objective: Objective) -> str:
    if objective.latest_value:
        return "green" if objective.meets_target else "red"
    return ""
