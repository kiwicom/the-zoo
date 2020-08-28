from typing import Dict, Union

import structlog
from jsonschema import ValidationError
from jsonschema import validate as schema_validate
from yaml import FullLoader, dump, load

from zoo.services.models import Service

log = structlog.get_logger()

ZOO_JSON_SCHEMA = """
    type: object
    properties:
        type:
            type: string
        name:
            type: string
        owner:
            type: string
        impact:
            type: ["string", "null"]
            enum: ["profit", "customers", "employees"]
        status:
            type: ["string", "null"]
            enum: ["beta", "production", "deprecated", "discontinued"]
        docs_url:
            type: ["string", "null"]
        slack_channel:
            type: ["string", "null"]
        sentry_project:
            type: ["string", "null"]
        sonarqube_project:
            type: ["string", "null"]
        pagerduty_url:
            type: ["string", "null"]
        pagerduty_service:
            type: string
        tags:
            type: array
            items:
                type: string
        environments:
            type: array
            items:
                type: object
                properties:
                    name:
                        type: string
                    dashboard_url:
                        type: ["string", "null"]
                    service_urls:
                        type: array
                        items:
                            type: string
                    health_check_url:
                        type: ["string", "null"]
    additionalProperties: false
    required:
        - type
        - name
        - owner
    """


def validate(yml: str) -> bool:
    try:
        schema_validate(load(yml, Loader=FullLoader), load(ZOO_JSON_SCHEMA, FullLoader))
    except ValidationError as err:
        log.info("repos.sync_zoo_yml.validation_error", error=err)
        return False
    else:
        return True


def parse(yaml: str) -> Union[Dict, None]:
    return load(yaml, Loader=FullLoader)


def generate(service: Service) -> str:
    result = {
        "type": "service",
        "name": service.name,
        "owner": service.owner,
        "impact": service.impact,
        "status": service.status,
        "docs_url": service.docs_url,
        "slack_channel": service.slack_channel,
        "sentry_project": service.sentry_project,
        "sonarqube_project": service.sonarqube_project,
        "pagerduty_url": service.pagerduty_url,
        "pagerduty_service": service.pagerduty_service,
        "tags": service.tags,
        "environments": [],
    }

    for env in service.environments.all():
        environ = {
            "name": env.name,
            "dashboard_url": env.dashboard_url,
            "health_check_url": env.health_check_url,
            "service_urls": env.service_urls,
        }
        result["environments"].append(environ)

    return dump(result, sort_keys=False)
