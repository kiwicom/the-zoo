from elasticsearch import Elasticsearch
from django.conf import settings

from zoo.analytics.models import Dependency
from zoo.services.models import Service
from zoo.utils import model_instance_to_json_object


class Indexer:

    def __init__(self):
        self.es = Elasticsearch(hosts=[settings.ELASTICSEARCH_HOST])
        self.models_to_index = [Service, Dependency]

    def index_specified_models(self):
        for model in self.models_to_index:
            for instance in model.objects.all():
                serialized_service = model_instance_to_json_object(instance)
                self.es.index(index=serialized_service['model'].split('.')[0],
                              doc_type=serialized_service['model'].split('.')[1],
                              id=serialized_service['pk'],
                              body=serialized_service['fields'])




