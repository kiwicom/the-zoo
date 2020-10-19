import meilisearch
import structlog
from django.apps import apps
from django.conf import settings
from django.views.generic import TemplateView

log = structlog.get_logger()


class MeiliSearchView(TemplateView):
    template_name = "search_overview.html"
    context_object_name = "context"
    per_page = 25

    @staticmethod
    def _objects_from_result(search_results, index, result_objects=None):
        if index["name"] not in result_objects.keys():
            result_objects[index["name"]] = []
        try:
            model = apps.get_model(index["uid"], index["name"])
            for result in search_results:
                result_objects[index["name"]].append(model.objects.get(pk=result["id"]))
        except LookupError:
            for result in search_results:
                result_objects[index["name"]].append(result["id"])

        return result_objects

    def _search(self, query_param):
        meili_client = meilisearch.Client(
            settings.MEILI_HOST, settings.MEILI_MASTER_KEY
        )
        indexes = meili_client.get_indexes()
        objects_to_return = {}
        for index in indexes:
            results = meili_client.get_index(index["uid"]).search(query_param)["hits"]
            objects_for_index = self._objects_from_result(
                results, index, objects_to_return
            )
            objects_to_return.update(objects_for_index)
        return objects_to_return

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if "q" in self.request.GET:
            results = self._search(self.request.GET["q"])
            context_data.update(results)
        return context_data
