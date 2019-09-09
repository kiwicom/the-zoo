from datetime import datetime, timedelta

from django.conf import settings
from django.http import Http404, JsonResponse
from pygerduty import exceptions
from pygerduty.v2 import PagerDuty


def _isoformat(dtime):
    return "%sZ" % dtime.isoformat()


def service_details(request, service_id):
    client = PagerDuty(settings.PAGERDUTY_TOKEN)
    week_ago = _isoformat(datetime.now() - timedelta(days=7))

    try:
        service = client.services.show(service_id, exclude=["teams", "integrations"])
    except exceptions.NotFound:
        raise Http404(f"Pagerduty service {service_id!r} not found")

    oncalls = client.oncalls.list(escalation_policy_ids=[service.escalation_policy.id])
    oncall_people = [oncall.user for oncall in oncalls if oncall.escalation_level == 1]

    incidents = list(client.incidents.list(service_ids=[service.id], since=week_ago))
    active_incidents = list(
        client.incidents.list(
            service_ids=[service.id], statuses=["acknowledged", "triggered"]
        )
    )

    return JsonResponse(
        {
            "id": service.id,
            "summary": service.summary,
            "html_url": service.html_url,
            "oncall": oncall_people[0].to_json() if oncall_people else None,
            "incidents": {
                "past_week_total": len(incidents),
                "active_total": len(active_incidents),
                "active": [
                    {
                        "id": incident.id,
                        "summary": incident.summary,
                        "description": incident.description,
                        "status": incident.status,
                        "html_url": incident.html_url,
                        "created_at": incident.created_at,
                        "color": "red" if incident.status == "triggered" else "yellow",
                    }
                    for incident in active_incidents
                ],
            },
        }
    )
