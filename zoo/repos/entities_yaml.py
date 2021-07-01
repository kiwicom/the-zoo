from typing import List, Union

import structlog
import yaml
from jsonschema import ValidationError
from jsonschema import validate as schema_validate
from yaml import FullLoader, dump, load_all

from zoo.repos.models import Repository

log = structlog.get_logger()


SCHEMAS = {
    "base_component": "zoo/entities/yaml_definitions/component_base.yaml",
    "service": "zoo/entities/yaml_definitions/component_service.yaml",
    "library": "zoo/entities/yaml_definitions/component_library.yaml",
}


def select_schema(entity):
    if entity["kind"].lower() == "component":
        if entity["spec"]["type"].lower() == "service":
            return "/Users/jaroslav.sevcik/work/the-zoo/zoo/components/yaml_definitions/service.yaml"
            # return SCHEMAS["service"]
        elif entity["spec"]["type"].lower() == "library":
            return "/Users/jaroslav.sevcik/work/the-zoo/zoo/components/yaml_definitions/library.yaml"
            # return SCHEMAS["library"]
        else:
            return "/Users/jaroslav.sevcik/work/the-zoo/zoo/components/yaml_definitions/component.yaml"
            # return SCHEMAS["base_component"]
    else:
        log.info("repos.sync_entity_yaml.no_schema_defined")


def validate(_yaml: str) -> bool:
    try:
        all_entities = load_all(_yaml, FullLoader)
        for entity in all_entities:  # list(list)
            schema = select_schema(entity[0])
            if not schema:
                raise ValidationError
            with open(schema, "r") as schema_file:
                schema_dict = yaml.load(schema_file, FullLoader)
                schema_validate(entity[0], schema_dict)
    except ValidationError as err:
        log.info("repos.sync_entity_yml.validation_error", error=err)
        return False
    else:
        return True


def parse(_yaml: str) -> Union[List, None]:
    return load_all(_yaml, Loader=FullLoader)


def generate_component_base(component):
    component_base_document = {
        "apiVersion": "v1alpha1",
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
        component_base_document["metadata"]["links"].append(link_document)

    return component_base_document


def generate_component_library(component_library, component_base_doc):
    component_base_doc["spec"] = {
        "type": "library",
        "lifecycle": component_library.library.lifecycle,
        "impact": component_library.library.impact,
        "analysis": [],
        "integrations": {
            "sonarqube_project": component_library.library.sonarqube_project,
            "slack_channel": component_library.library.slack_channel,
        },
    }

    return component_base_doc


def generate_component_service(component_service, component_base_doc):
    component_base_doc["spec"] = {
        "type": "service",
        "lifecycle": component_service.service.lifecycle,
        "impact": component_service.service.impact,
        "analysis": [],
        "environments": [],
        "integrations": {
            "sonarqube_project": component_service.service.sonarqube_project,
            "slack_channel": component_service.service.slack_channel,
            "sentry": component_service.service.sentry_project,
        },
    }

    for environment in component_service.service.environments.all():
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
        component_base_doc["spec"]["environments"].append(environment_document)

    return component_base_doc


def generate(repository: Repository) -> str:
    results = []
    for entity in repository.entities.all():
        if entity.kind != "component":
            return NotImplemented
        component_base_document = generate_component_base(entity)
        if entity.type == "library":
            component_library_document = generate_component_library(
                entity, component_base_document
            )
            results.append(component_library_document)
        elif entity.type == "service":
            component_service_document = generate_component_service(
                entity, component_base_document
            )
            results.append(component_service_document)
        else:
            return NotImplemented
    return dump(results, sort_keys=False)
