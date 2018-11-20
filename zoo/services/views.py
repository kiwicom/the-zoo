from collections import defaultdict
from datetime import timedelta
import re
from typing import Dict, List

from django.db.models import Q, query, Sum
from django.http import Http404
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from djangoql.exceptions import DjangoQLError
from djangoql.queryset import apply_search
import structlog

from . import forms, models
from ..auditing.models import Issue

log = structlog.get_logger()


class ServiceMixin:
    def get_object(self, queryset=None):
        """Return the service based on owner and name from the URL."""
        if queryset is None:
            queryset = self.get_queryset()

        try:
            return queryset.get(
                owner_slug=self.kwargs["owner_slug"], name_slug=self.kwargs["name_slug"]
            )

        except queryset.model.DoesNotExist:
            raise Http404("Service.DoesNotExist")


class ServiceCreate(CreateView):
    form_class = forms.ServiceForm
    model = form_class.Meta.model


class ServiceDetail(ServiceMixin, DetailView):
    model = models.Service

    def generate_sentry_histogram(
        self, sentry_issues: query.QuerySet
    ) -> Dict[int, List[int]]:
        result = defaultdict(list)

        for issue in sentry_issues:
            last_two_weeks = sorted(issue.stats.all(), key=lambda x: x.timestamp)[:14]
            max_events_count = max([day.count for day in last_two_weeks])

            for day in last_two_weeks:
                bar_height = (
                    max(day.count / max_events_count, 0.175) if day.count else 0
                )

                result[issue.id].append(
                    {
                        "value": bar_height,
                        "tooltip": f"""
                            <h4>{day.timestamp.strftime('%d/%m/%Y')}</h4>
                            <strong>{day.count}</strong> events
                        """,
                    }
                )

        return dict(result)

    def calculate_weekly_sentry_stats(
        self, sentry_issues: query.QuerySet
    ) -> Dict[str, int]:
        one_week_ago = timezone.now().date() - timedelta(days=7)
        last_week_issues = sentry_issues.filter(last_seen__gte=one_week_ago).annotate(
            freq=Sum("stats__count", filter=Q(stats__timestamp__gte=one_week_ago))
        )
        weekly_events = last_week_issues.aggregate(Sum("freq"))["freq__sum"] or 0
        weekly_users = last_week_issues.aggregate(Sum("users"))["users__sum"] or 0

        return {"events": weekly_events, "users": weekly_users}

    def get_sentry_context(self):
        ISSUE_ORDER = {
            models.SentryIssueCategory.STALE.value: 0,
            models.SentryIssueCategory.DECAYING.value: 1,
            models.SentryIssueCategory.SPOILED.value: 2,
        }

        sentry_issues_queryset = self.object.sentry_issues.prefetch_related(
            "stats"
        ).all()

        if not sentry_issues_queryset.exists():
            return None

        all_sentry_issues = sentry_issues_queryset.order_by("-last_seen")

        problematic_sentry_issues = sorted(
            sentry_issues_queryset.exclude(
                category=models.SentryIssueCategory.FRESH.value
            ).all(),
            key=lambda k: (ISSUE_ORDER[k.category], k.last_seen),
        )

        issue_histogram = self.generate_sentry_histogram(all_sentry_issues)
        weekly_stats = self.calculate_weekly_sentry_stats(all_sentry_issues)

        return {
            "weekly_events": weekly_stats["events"],
            "weekly_users": weekly_stats["users"],
            "issues": [
                {
                    "id": issue.id,
                    "instance": issue,
                    "histogram": issue_histogram[issue.id],
                }
                for issue in problematic_sentry_issues
            ],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object.repository:
            context["issue_count"] = self.object.repository.issues.filter(
                status=Issue.Status.NEW.value
            ).count()

        context["sentry_data"] = self.get_sentry_context()

        return context


class ServiceList(ListView):
    model = models.Service
    paginate_by = 50

    def get_queryset(self):
        queryset = self.model.objects.select_related("repository", "datacenter")
        queryterm = self.request.GET.get("q", None)

        SIMPLE_QUERY_PATTERN = r"^[\w-]+$"
        URL_QUERY_PATTERN = r"^https?[:][/][/]\S+$"

        if queryterm:
            if re.match(SIMPLE_QUERY_PATTERN, queryterm):
                queryset = queryset.filter(
                    Q(name__icontains=queryterm)
                    | Q(owner__icontains=queryterm)
                    | Q(status__icontains=queryterm)
                    | Q(impact__icontains=queryterm)
                    | Q(datacenter__provider__icontains=queryterm)
                )

            elif re.match(URL_QUERY_PATTERN, queryterm):
                queryset = queryset.filter(
                    Q(docs_url__icontains=queryterm)
                    | Q(service_url__icontains=queryterm)
                    | Q(health_check_url__icontains=queryterm)
                )

            else:
                try:
                    queryset = apply_search(queryset, queryterm, models.ServiceQLSchema)
                except DjangoQLError:
                    log.exception("services.query_error", queryterm=queryterm)
                    return self.model.objects.none()

        return queryset.order_by("name")


class ServiceUpdate(ServiceMixin, UpdateView):
    form_class = forms.ServiceForm
    model = form_class.Meta.model
