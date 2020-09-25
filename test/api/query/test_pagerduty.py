import pytest
from graphql_relay import to_global_id

pytestmark = pytest.mark.django_db


def test_pagerduty_service(snapshot, mocker, call_api, service_factory):
    service_factory(
        id=10,
        owner="bradltwat",
        name="allen-nobles",
        status="fixed",
        impact="sales",
        slack_channel="https://gitlab.slack",
        pagerduty_service="services/1A2B3",
        docs_url="https://docs/skypicker/docs/",
    )
    id = to_global_id("Service", 10)

    mocker.patch(
        "zoo.pagerduty.tasks.get_oncall_info",
        return_value={
            "id": "1A2B3",
            "summary": "service_sumary",
            "html_url": "https://example.com/service/1",
            "oncall_person": mocker.Mock(
                id="USER1",
                type="user",
                summary="user_summary",
                html_url="https://example.com/users/1",
            ),
            "past_week_total": 2,
            "all_active_incidents": [
                mocker.Mock(
                    id="INCIDENT1",
                    summary="incident_summary",
                    description="incident_description",
                    status="triggered",
                    html_url="https://example.com/incidents/1",
                    created_at="2020-04-28T11:39:52Z",
                )
            ],
        },
    )

    query = f"""
    query {{
        node (id:"{id}") {{
            ... on Service {{
                pagerdutyService {{
                    id,
                    summary,
                    htmlUrl,
                    oncallPerson {{
                        id,
                        type,
                        summary,
                        htmlUrl,
                    }},
                    pastWeekTotal,
                    allActiveIncidents(first: 3) {{
                        totalCount,
                        edges {{
                            node {{
                                id,
                                summary,
                                description,
                                status,
                                htmlUrl,
                                createdAt,
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
    """
    response = call_api(query)
    snapshot.assert_match(response)
