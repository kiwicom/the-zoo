import json

import structlog
from elasticsearch import Elasticsearch, ElasticsearchException
from django.conf import settings
from zoo.base import redis

from zoo.analytics.models import Dependency
from zoo.services.models import Service
from zoo.utils import model_instance_to_json_object


log = structlog.get_logger()


class Indexer:

    def __init__(self):
        self.es = Elasticsearch(hosts=[settings.ELASTICSEARCH_HOST])
        self.models_to_index = [Service, Dependency]

    def index_specified_models(self):
        for model in self.models_to_index:
            for instance in model.objects.all():
                serialized_service = model_instance_to_json_object(instance)
                try:
                    self.es.index(index=serialized_service['model'].split('.')[0],
                                  doc_type=serialized_service['model'].split('.')[1],
                                  id=serialized_service['pk'],
                                  body=serialized_service['fields'])
                except ElasticsearchException as exception:
                    log.error(f'ES Failed to Index Model Instance - {model}, {instance} because of'
                              f'{repr(exception)}')

    def index_openapi(self):
        redis_conn = redis.get_connection()
        definition_keys = redis_conn.keys()
        for key in definition_keys:
            definition = redis_conn.get(key)
            json_definitions = json.loads(definition)
            title = '.'.join([definition['info']['title'] for definition in json_definitions])
            description = '.'.join([definition['info']['description'] for definition in json_definitions])
            paths = self._get_all_paths(json_definitions)
            try:
                self.es.index(index='open-api',
                                    doc_type='schema',
                                    id=key,
                                    body={
                                        'title': title,
                                        'description': description,
                                        'endpoints': paths,
                                    })
            except ElasticsearchException as exception:
                log.error(f'ES Failed to Index Open Api definition - {key} because of '
                          f'{repr(exception)}')

    @staticmethod
    def _get_all_paths(definitions):
        paths = []
        for definition in definitions:
            for path in list(definition['paths'].keys()):
                paths.append(path)
        return paths
