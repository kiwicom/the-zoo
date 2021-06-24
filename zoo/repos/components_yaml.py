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
    if component["spec"]["type"].lower() == "service":
        return "/Users/jaroslav.sevcik/work/the-zoo/zoo/components/yaml_definitions/service.yaml"
        # return SCHEMAS["service"]
    elif component["spec"]["type"].lower() == "library":
        return "/Users/jaroslav.sevcik/work/the-zoo/zoo/components/yaml_definitions/library.yaml"
        # return SCHEMAS["library"]
    else:
        return "/Users/jaroslav.sevcik/work/the-zoo/zoo/components/yaml_definitions/component.yaml"
        # return SCHEMAS["base_component"]


def validate(_yaml: str) -> bool:
    try:
        all_components = load_all(_yaml, FullLoader)
        for component in all_components:  # list(list)
            schema = select_schema(component[0])
            if not schema:
                raise ValidationError
            with open(schema, "r") as schema_file:
                schema_dict = yaml.load(schema_file, FullLoader)
                schema_validate(component[0], schema_dict)
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
            "spec": {"type": component.type},
        }

        for link in component.links.all():
            link_document = {"name": link.name, "url": link.url, "icon": link.icon}
            component_document["metadata"]["links"].append(link_document)

        # Library component
        if component.library:
            component_document["spec"] = {
                "type": "library",
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
                "type": "service",
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
