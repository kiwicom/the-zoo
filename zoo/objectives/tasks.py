import hashlib
from decimal import Decimal

import arrow
import requests
import structlog
from celery import shared_task
from datadog import api, initialize
from django.conf import settings

from ..base.http import session
from . import models

log = structlog.get_logger()
initialize(api_key=settings.DATADOG_API_KEY, app_key=settings.DATADOG_APP_KEY)


def check_datadog(objective: models.Objective, query_datetime: arrow.Arrow) -> float:
    response = api.Metric.query(
        start=query_datetime.shift(days=-30).timestamp,
        end=query_datetime.timestamp,
        query=objective.indicator_query,
    )

    series = response["series"][0]
    point = series["pointlist"][0]
    _, point_value = point
    return round(Decimal(point_value), 4)


def check_pingdom(objective: models.Objective, query_datetime: arrow.Arrow) -> float:
    api_url = (
        f"https://api.pingdom.com/api/2.1/summary.average/{objective.indicator_query}"
    )

    response = session.get(
        api_url,
        auth=(settings.PINGDOM_EMAIL, settings.PINGDOM_PASS),
        headers={"App-Key": settings.PINGDOM_APP_KEY},
        params={
            "from": query_datetime.shift(days=-30).timestamp,
            "to": query_datetime.timestamp,
            "includeuptime": "true",
        },
    )

    response.raise_for_status()

    status = response.json()["summary"]["status"]
    total_time = sum(status.values())

    return round(Decimal(status["totalup"] / total_time), 4)


available_services = {
    models.IndicatorSource.DATADOG.value: check_datadog,
    models.IndicatorSource.PINGDOM.value: check_pingdom,
}


@shared_task
def take_objective_snapshots(objective_id: int) -> None:
    try:
        objective = models.Objective.objects.get(id=objective_id)

    except models.Objective.DoesNotExist:
        log.info(
            "take_objective_snapshots.objective_not_found", objective_id=objective_id
        )
        raise

    now = arrow.now()
    checker = available_services[objective.indicator_source]

    try:
        indicator_value = checker(objective, now)
    except requests.RequestException:
        log.exception(
            "take_objective_snapshots.invalid_api_response",
            objective=objective,
            checker=checker,
        )
        raise

    snapshot = models.ObjectiveSnapshot(
        objective=objective, timestamp=now.datetime, indicator_value=indicator_value
    )
    snapshot.full_clean()
    snapshot.save()


@shared_task
def schedule_objective_snapshots():
    for objective in models.Objective.objects.all():
        pk_hash = hashlib.sha256(f"objectives-{objective.indicator_query}".encode())
        delay_s = int(pk_hash.hexdigest(), 16) % (60 * 60)

        take_objective_snapshots.apply_async(
            args=(objective.id,), countdown=delay_s, expires=delay_s + (60 * 60 * 24)
        )
