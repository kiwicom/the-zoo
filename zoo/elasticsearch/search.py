import structlog
from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from django.apps import apps

from zoo.services.models import Service

log = structlog.get_logger()


class ElasticSearchView(TemplateView):
    template_name = "search_overview.html"
    context_object_name = "context"
    per_page = 25

    @staticmethod
    def _objects_from_result(es_result):
        result_objects = {}
        print(es_result)
        for result in es_result['hits']['hits']:
            if result['_type'] == 'schema':
                if 'service_detail_urls' not in result_objects.keys():
                    result_objects['service_detail_urls'] = []
                try:
                    remote_repo_id = int(result['_id'].split('-')[-1])
                    services = Service.objects.filter(repository__remote_id=remote_repo_id)
                    for service in services:
                        result_objects['service_detail_urls'].append(service.get_absolute_url())
                except Service.DoesNotExist as err:
                    log.info(f'Service With Remote Gitlab ID - {remote_repo_id} does not exists.',
                             error=err)
            else:
                if result['_type'] not in result_objects.keys():
                    result_objects[result['_type']] = []
                result_objects[result['_type']].append(
                    apps.get_model(result['_index'], result['_type']).objects.get(
                        id=result['_id']
                    )
                )
        return result_objects

    def _search(self, query_param):
        query = {
            "query": {
                "multi_match": {
                    "query": query_param
                }
            }
        }
        es = Elasticsearch(hosts=[settings.ELASTICSEARCH_HOST])
        result = es.search(body=query, index='_all')
        return self._objects_from_result(result)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if "q" in self.request.GET:
            results = self._search(self.request.GET["q"])
            context_data.update(results)
        print(context_data)
        return context_data
