from datetime import datetime, timedelta
import httpretty
import json
import pytest

from django.http import Http404, JsonResponse
from freezegun import freeze_time
from zoo.pagerduty import views as uut


@httpretty.activate
@freeze_time("2019-09-08")
def test_pagerduty_service_details(mocker):
    mocker.patch("zoo.pagerduty.views.settings.PAGERDUTY_TOKEN", "test-token")

    base_api_url = "https://api.pagerduty.com"
    escalation_policy_id = "POLICY1"

    service = {
        "id": "SERVICE1",
        "summary": "test",
        "html_url": "url",
        "escalation_policy": {"id": escalation_policy_id},
    }
    oncall_user = {"user": {"id": "USER1"}, "escalation_level": 1}

    incident_resolved = {
        "id": "INCIDENTRESOLVED1",
        "summary": "incident",
        "description": "test description",
        "status": "resolved",
        "html_url": "url",
        "created_at": uut._isoformat(datetime.now() - timedelta(days=1)),
    }
    incident_active = {
        "id": "INCIDENTACTIVE1",
        "summary": "incident",
        "description": "test description",
        "status": "triggered",
        "html_url": "url",
        "created_at": uut._isoformat(datetime.now()),
    }

    httpretty.register_uri(
        httpretty.GET,
        f"{base_api_url}/services/{service['id']}",
        body=json.dumps({"service": service}),
    )

    escalation_policy_ids = f"escalation_policy_ids[]={escalation_policy_id}"
    oncalls_url = f"{base_api_url}/oncalls?{escalation_policy_ids}"

    httpretty.register_uri(
        httpretty.GET,
        oncalls_url + "&limit=25&offset=0",
        body=json.dumps({"oncalls": [oncall_user]}),
        match_querystring=True,
    )
    httpretty.register_uri(
        httpretty.GET,
        oncalls_url + "&limit=25&offset=1",
        body=json.dumps({"oncalls": []}),
        match_querystring=True,
    )

    since = f"since={uut._isoformat(datetime.now() - timedelta(days=7))}"
    service_ids = f"service_ids[]={service['id']}"
    incidents_url = f"{base_api_url}/incidents?{service_ids}&{since}"

    httpretty.register_uri(
        httpretty.GET,
        incidents_url + "&limit=25&offset=0",
        body=json.dumps({"incidents": [incident_resolved, incident_active]}),
        match_querystring=True,
    )
    httpretty.register_uri(
        httpretty.GET,
        incidents_url + "&limit=25&offset=2",
        body=json.dumps({"incidents": []}),
        match_querystring=True,
    )

    statuses = "statuses[]=acknowledged&statuses[]=triggered"
    incidents_active_url = f"{base_api_url}/incidents?{service_ids}&{statuses}"

    httpretty.register_uri(
        httpretty.GET,
        incidents_active_url + "&limit=25&offset=0",
        body=json.dumps({"incidents": [incident_active]}),
        match_querystring=True,
    )
    httpretty.register_uri(
        httpretty.GET,
        incidents_active_url + "&limit=25&offset=1",
        body=json.dumps({"incidents": []}),
        match_querystring=True,
    )

    response = uut.service_details(mocker.Mock(), service["id"])

    assert isinstance(response, JsonResponse)
    assert json.loads(response.content) == {
        "id": service["id"],
        "summary": service["summary"],
        "html_url": service["html_url"],
        "oncall": oncall_user["user"],
        "incidents": {
            "past_week_total": 2,
            "active_total": 1,
            "active": [
                {
                    "id": incident_active["id"],
                    "summary": incident_active["summary"],
                    "description": incident_active["description"],
                    "status": incident_active["status"],
                    "html_url": incident_active["html_url"],
                    "created_at": incident_active["created_at"],
                    "color": "red",
                }
            ],
        },
    }


@httpretty.activate
def test_pagerduty_service_details__not_found(mocker):
    mocker.patch("zoo.pagerduty.views.settings.PAGERDUTY_TOKEN", "test-token")

    base_api_url = "https://api.pagerduty.com"
    service_id = "NOTFOUND"

    httpretty.register_uri(
        httpretty.GET, f"{base_api_url}/services/{service_id}", body="", status=404
    )

    with pytest.raises(Http404):
        uut.service_details(mocker.Mock(), service_id)
