from math import ceil

import structlog
from django.apps import apps
from django.views.generic import TemplateView

from .meili_client import meili_client

log = structlog.get_logger()


class MeiliSearchView(TemplateView):
    template_name = "search_overview.html"
    context_object_name = "context"
    meili_limit = 20

    @staticmethod
    def _objects_from_result(search_results, index, result_objects=None):
        try:
            model = apps.get_model(index["uid"], index["name"])
            for result in search_results:
                key = index["name"].lower()
                if key not in result_objects.keys():
                    result_objects[key] = []
                result_objects[key].append(model.objects.get(pk=result["id"]))
        except LookupError:
            for result in search_results:
                result_objects[index["name"].lower()].append(result["id"])

        return result_objects

    def _search(self, search_query, index_type, offset=0, limit=meili_limit):
        objects_to_return = {}
        new_offset, total_hits = 0, 0
        indexes = meili_client.get_indexes()
        for index in indexes:
            results = meili_client.get_index(index["uid"]).search(
                query=search_query, opt_params={"offset": offset, "limit": limit}
            )
            objects_to_return[f"total_{index['name'].lower()}"] = results["nbHits"]

            if index_type == index["uid"]:
                new_offset = results["offset"]
                total_hits = results["nbHits"]
                objects_for_index = self._objects_from_result(
                    results["hits"], index, objects_to_return
                )
                objects_to_return.update(objects_for_index)

        return objects_to_return, new_offset, total_hits

    def convert_meili_to_pages(self, total_hits, offset, limit=meili_limit):
        if total_hits < limit:
            return {
                "total_pages": 1,
                "current_page": 1,
                "next_page": None,
                "previous_page": None,
            }

        total_pages = ceil(total_hits / limit)
        current_page = ceil((offset + limit) / limit)
        next_page = None if total_pages == current_page else current_page + 1
        previous_page = None if next_page == 1 else current_page - 1

        return {
            "total_pages": total_pages,
            "current_page": current_page,
            "next_page": next_page,
            "previous_page": previous_page,
        }

    def convert_page_to_offset(self, page, limit=meili_limit):
        return int((page * limit) - limit)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if "q" in self.request.GET:
            results, offset, total_hits = self._search(
                search_query=self.request.GET["q"],
                index_type=self.request.GET.get("t", "services"),
                offset=self.convert_page_to_offset(
                    int(self.request.GET.get("page", 1))
                ),
            )
            context_data.update(results)
            context_data["search_query"] = self.request.GET["q"]
            context_data["search_type"] = self.request.GET.get("t", "services")
            context_data["pagination"] = self.convert_meili_to_pages(total_hits, offset)

        context_data["project_links"] = [
            "Support",
            "Repository",
            "Dashboard",
            "Alerts",
            "Documentation",
        ]
        return context_data
