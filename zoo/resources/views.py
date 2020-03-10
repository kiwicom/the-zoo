from typing import List

from django.db.models import Count, Prefetch, Q
from django.views.generic import DetailView, ListView, TemplateView

from ..analytics.models import Dependency, DependencyType, DependencyUsage


class BaseResourceOverview(ListView):
    model = Dependency
    paginate_by = 50
    template_name = "dependency_overview.html"
    dependency_types: List[DependencyType] = []

    def filter_queryset(self, queryset):
        return queryset.filter(Q())

    def get_queryset(self):
        return self.filter_queryset(
            super()
            .get_queryset()
            .filter(type__in=[dep.value for dep in self.dependency_types])
            .prefetch_related("depusage")
            .annotate(usage_count=Count("depusage"))
            .order_by("-usage_count")
        )


class LibraryOverview(BaseResourceOverview):
    dependency_types = [DependencyType.PY_LIB, DependencyType.JS_LIB]
    title = "Internal libraries"
    icon = "book"

    def filter_queryset(self, queryset):
        return queryset.filter(name__startswith="kiwi")


class DependencyOverview(BaseResourceOverview):
    title = "Public libraries"
    icon = "book"

    dependency_types = [DependencyType.PY_LIB, DependencyType.JS_LIB]

    def filter_queryset(self, queryset):
        return queryset.exclude(name__startswith="kiwi")


class DependencyDetail(DetailView):
    template_name = "dependency_detail.html"
    model = Dependency

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                Prefetch(
                    "depusage",
                    DependencyUsage.objects.all()
                    .order_by("-version")
                    .prefetch_related("repo__services"),
                )
            )
        )


class CiTemplateOverview(TemplateView):
    template_name = "ci_template_overview.html"


class ProjectTemplateOverview(TemplateView):
    template_name = "project_template_overview.html"


class LanguageOverview(BaseResourceOverview):
    dependency_types = [DependencyType.LANG]
    title = "Languages"
    icon = "stream"
