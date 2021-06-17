from typing import List, Union

import structlog
import yaml
from jsonschema import ValidationError
from jsonschema import validate as schema_validate
from yaml import FullLoader, dump, load_all

from zoo.repos.models import Repository

log = structlog.get_logger()


SCHEMAS = {
    "base_component": "zoo/components/yaml_definitions/component.yaml",
    "service": "zoo/components/yaml_definitions/service.yaml",
    "library": "zoo/components/yaml_definitions/library.yaml",
}


def select_schema(component):
    try:
        if component["spec"]["type"].lower() == "service":
            return yaml.load(SCHEMAS["service"], Loader=yaml.FullLoader)
        elif component["spec"]["type"].lower() == "library":
            return yaml.load(SCHEMAS["library"], Loader=yaml.FullLoader)
    except KeyError:
        return yaml.load(SCHEMAS["base_component"], Loader=yaml.FullLoader)


def validate(_yaml: str) -> bool:
    try:
        all_components = load_all(_yaml, FullLoader)
        for component in all_components:
            schema = select_schema(component)
            schema_validate(component, schema)
    except ValidationError as err:
        log.info("repos.sync_entity_yml.validation_error", error=err)
        return False
    else:
        return True


def parse(_yaml: str) -> Union[List, None]:
    return load_all(_yaml, Loader=FullLoader)


def generate(repository: Repository) -> str:
    results = []
    for component in repository.components.all():
        # Base component structure
        component_document = {
            "apiVersion": "v1alpha1",  # TODO: change
            "kind": "component",
            "metadata": {
                "name": component.name,
                "owner": component.owner,
                "group": {
                    "product_owner": component.group.product_owner,
                    "project_owner": component.group.project_owner,
                    "maintainers": component.group.maintainers,
                },
                "description": component.description,
                "tags": component.tags,
                "links": [],
            },
        }

        for link in component.links.all():
            link_document = {"name": link.name, "url": link.url, "icon": link.icon}
            component_document["metadata"]["links"].append(link_document)

        # Library component
        if component.library:
            component_document["spec"] = {
                "lifecycle": component.library.lifecycle,
                "impact": component.library.impact,
                "analysis": [],
                "integrations": {
                    "sonarqube_project": component.library.sonarqube_project,
                    "slack_channel": component.library.slack_channel,
                },
            }
        # Service component
        elif component.service:
            component_document["spec"] = {
                "lifecycle": component.service.lifecycle,
                "impact": component.service.impact,
                "analysis": [],
                "environments": [],
                "integrations": {
                    "sonarqube_project": component.service.sonarqube_project,
                    "slack_channel": component.service.slack_channel,
                    "sentry": component.service.sentry_project,
                },
            }

            for environment in component.service.environments.all():
                environment_document = {
                    "name",
                    environment.name,
                    "dashboard_url",
                    environment.dashboard_url,
                    "service_urls",
                    environment.service_urls,
                    "health_check_url",
                    environment.health_check_url,
                }
                component_document["spec"]["environments"].append(environment_document)
        results.append(component_document)
    return dump(results, sort_keys=False)
