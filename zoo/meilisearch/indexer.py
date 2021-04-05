import json
from enum import Enum

import meilisearch
import structlog
from django.conf import settings

from zoo.analytics.models import Dependency
from zoo.base import redis
from zoo.services.models import Service
from zoo.utils import model_instance_to_json_object

log = structlog.get_logger()


class IndexType(Enum):
    Service = "services"
    Dependency = "analytics"


class Indexer:
    def __init__(self):
        self.meiliclient = meilisearch.Client(
            settings.MEILI_HOST, settings.MEILI_MASTER_KEY
        )
        self.models_to_index = [
            (Service, IndexType.Service.value),
            (Dependency, IndexType.Dependency.value),
        ]

    def index_specified_models(self):
        for model, index_name in self.models_to_index:
            for instance in model.objects.all():
                serialized_model_instance = model_instance_to_json_object(instance)
                try:
                    serialized_model_instance["fields"][
                        "id"
                    ] = serialized_model_instance["pk"]
                    self.meiliclient.get_or_create_index(
                        index_name, {"name": model.__name__}
                    ).update_documents([serialized_model_instance["fields"]])
                # deepcode ignore W0703: Multiple Possible Exceptions
                except Exception as err:
                    log.info(
                        "Failed to Index Model Instance",
                        error=err,
                        model=model,
                        instance=instance,
                    )

    def index_openapi(self):
        redis_conn = redis.get_connection()
        definition_keys = redis_conn.keys()
        for key in definition_keys:
            definition = redis_conn.get(key)
            json_definition = json.loads(definition)
            try:
                json_definition["id"] = key
                self.meiliclient.get_or_create_index("open-api").update_documents(
                    [{json_definition}]
                )
            # deepcode ignore W0703: Multiple Possible Exceptions
            except Exception as err:
                log.info("Failed to Index OpenAPI", error=err, key=key)

    @staticmethod
    def _get_all_paths(definitions):
        paths = []
        for definition in definitions:
            for path in list(definition["paths"].keys()):
                paths.append(path)
        return paths
