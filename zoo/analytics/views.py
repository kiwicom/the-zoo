from collections import Counter
from itertools import islice
import json

from arrow import Arrow
from django.core.paginator import Paginator
from django.db.models import Count, Prefetch, Q
from django.utils import timezone
from django.views.generic import TemplateView

from . import models
from ..services import models as servicemodels

COLOR_PALETTE = [
    "#117510",
    "#f38551",
    "#5d2b58",
    "#8E24AA",
    "#d39459",
    "#d00188",
    "#84fd9c",
    "#cd9e67",
    "#72cccb",
    "#c51900",
    "#475963",
    "#077ffe",
    "#55cf29",
    "#9d07e8",
    "#3db8b1",
    "#ff746e",
]


def chunk(collection, pieces: int) -> iter:
    iterable = iter(collection)
    return iter(lambda: tuple(islice(iterable, int(len(collection) / pieces))), ())


class AnalyticsOverview(TemplateView):
    template_name = "analytics_overview.html"
    context_object_name = "context"
    per_page = 25

    def _get_queryset(self):
        self.per_page = self.request.GET.get("per_page", self.per_page)

        time_axis_origin = Arrow.fromdatetime(timezone.now()).shift(years=-1).datetime

        queryset = (
            models.Dependency.objects.annotate(dep_count=Count("depusage"))
            .prefetch_related(
                Prefetch(
                    "snapshots",
                    queryset=models.DependencySnapshot.objects.filter(
                        timestamp__gte=time_axis_origin
                    ).order_by("timestamp"),
                )
            )
            .prefetch_related("depusage")
            .all()
            .order_by("-dep_count")
        )

        if "q" in self.request.GET:
            queryset = queryset.filter(
                Q(name__icontains=self.request.GET["q"])
                | Q(depusage__repo__services__name__icontains=self.request.GET["q"])
            )

        if "type" in self.request.GET:
            queryset = queryset.filter(type=self.request.GET["type"])

        paginator = Paginator(queryset, self.per_page)
        return paginator.get_page(self.request.GET.get("page", 1))

    @staticmethod
    def _get_usage_chart_stats(dependency: models.Dependency) -> dict:
        snapshots = dependency.snapshots.all()
        labels = []
        series = []

        for snapshot_period in chunk(list(snapshots), 14):
            snapshot = snapshot_period[0]
            labels.append(snapshot.timestamp.strftime("%d/%m/%Y"))
            series.append(snapshot.dep_usages_num)

        return {
            "id": f"usage-chart-{dependency.id}",
            "data": json.dumps({"labels": labels, "series": series}),
        }

    @staticmethod
    def _get_version_chart_stats(dependency: models.Dependency) -> dict:

        version_frequency = Counter(
            [usage.version for usage in dependency.depusage.all()]
        )

        return {
            "id": f"version-chart-{dependency.id}",
            "data": json.dumps(
                [
                    {
                        "backgroundColor": COLOR_PALETTE[index % len(COLOR_PALETTE)],
                        "data": [version_frequency.get(version) / dependency.dep_count],
                        "label": f"{version}" if version else "Unknown",
                    }
                    for index, version in enumerate(version_frequency)
                ]
            ),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_page = self._get_queryset()

        context["page_obj"] = current_page

        if "q" in self.request.GET:
            context["services"] = servicemodels.Service.objects.filter(
                name__icontains=self.request.GET["q"]
            )

        context["dependency_types"] = [option.value for option in models.DependencyType]
        context["dependencies"] = [
            {
                "id": dependency.id,
                "instance": dependency,
                "health": dependency.health_status,
                "internal": dependency.name.startswith("kw."),
                "version_chart": self._get_version_chart_stats(dependency),
                "usage_chart": self._get_usage_chart_stats(dependency),
            }
            for dependency in current_page
        ]

        return context
