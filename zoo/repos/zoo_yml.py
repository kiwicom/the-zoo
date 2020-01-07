from typing import Dict, Union

import structlog
from jsonschema import ValidationError
from jsonschema import validate as schema_validate
from yaml import FullLoader, load

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
            type: string
            enum: ["profit", "customers", "employees"]
        status:
            type: string
            enum: ["beta", "production", "deprecated", "discontinued"]
        docs_url:
            type: string
        slack_channel:
            type: string
        sentry_project:
            type: string
        sonarqube_project:
            type: string
        pagerduty_url:
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
                        type: string
                    service_urls:
                        type: array
                        items:
                            type: string
                    health_check_url:
                        type: string
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
