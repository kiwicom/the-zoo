from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from django.apps import apps


class ElasticSearchView(TemplateView):
    template_name = "search_overview.html"
    context_object_name = "context"
    per_page = 25

    @staticmethod
    def _objects_from_result(es_result):
        model_instances = {}
        print(es_result)
        for result in es_result['hits']['hits']:
            if result['_type'] not in model_instances.keys():
                model_instances[result['_type']] = []
            model_instances[result['_type']].append(
                apps.get_model(result['_index'], result['_type']).objects.get(
                    id=result['_id']
                )
            )
        return model_instances

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
            for model, instances in results.items():
                if model not in context_data.keys():
                    context_data[model] = []
                context_data[model].append(instances)
        return context_data

