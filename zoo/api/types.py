import graphene
import structlog
from django.core.exceptions import ObjectDoesNotExist
from graphene.relay import Connection, ConnectionField, Node
from graphene.types.json import JSONString
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from ..analytics import models as analytics_models
from ..auditing import check_discovery
from ..auditing import models as auditing_models
from ..pagerduty.tasks import get_oncall_info
from ..repos import models as repos_models
from ..services import models as services_models
from .paginator import Paginator
from .utils import CheckResultStatus

log = structlog.get_logger()

IssueStatusEnum = graphene.Enum.from_enum(auditing_models.Issue.Status)
IssueSeverityEnum = graphene.Enum.from_enum(check_discovery.Severity)
IssueEffortEnum = graphene.Enum.from_enum(check_discovery.Effort)


class Issue(DjangoObjectType, interfaces=[Node]):
    repository = graphene.Field(lambda: Repository)

    class Meta:
        model = auditing_models.Issue
        filter_fields = ["kind_key"]


class Environment(DjangoObjectType, interfaces=[Node]):
    service_urls = graphene.List(graphene.String)
    service = graphene.Field(lambda: Service)

    class Meta:
        model = services_models.Environment
        filter_fields = ["name"]


class EnvironmentConnection_(Connection):
    total_count = graphene.Int()

    class Meta:
        node = Environment


class ActiveIncident(graphene.ObjectType):
    id = graphene.String()
    summary = graphene.String()
    description = graphene.String()
    status = graphene.String()
    html_url = graphene.String()
    created_at = graphene.String()
    color = graphene.String()

    @classmethod
    def from_object(cls, incident):
        return cls(
            id=incident.id,
            summary=incident.summary,
            description=incident.description,
            status=incident.status,
            html_url=incident.html_url,
            created_at=incident.created_at,
            color="red" if incident.status == "triggered" else "yellow",
        )


class ActiveIncidentConnection(Connection):
    total_count = graphene.Int()

    class Meta:
        node = ActiveIncident


class OncallPerson(graphene.ObjectType):
    id = graphene.String()
    type = graphene.String()
    summary = graphene.String()
    html_url = graphene.String()

    @classmethod
    def from_object(cls, user):
        return cls(
            id=user.id,
            type=user.type,
            summary=user.summary,
            html_url=user.html_url,
        )


class PagerdutyInfo(graphene.ObjectType):
    id = graphene.String()
    summary = graphene.String()
    html_url = graphene.String()
    oncall_person = graphene.Field(lambda: OncallPerson)
    past_week_total = graphene.Int()
    all_active_incidents = ConnectionField(ActiveIncidentConnection)

    def resolve_all_active_incidents(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        edges = []

        total = len(self.all_active_incidents)
        page_info = paginator.get_page_info(total)

        for i, issue in enumerate(
            self.all_active_incidents[  # pylint: disable=E1136
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = ActiveIncident.from_object(issue)
            edges.append(ActiveIncidentConnection.Edge(node=node, cursor=cursor))

        return ActiveIncidentConnection(
            page_info=page_info, edges=edges, total_count=total
        )


class HistogramItem(graphene.ObjectType):
    name = graphene.String()
    value = graphene.String()

    class Meta:
        interfaces = (Node,)


class HistogramItemConnection(Connection):
    total_count = graphene.Int()

    class Meta:
        node = HistogramItem


class SentryIssue(DjangoObjectType, interfaces=[Node]):
    class Meta:
        model = services_models.SentryIssue
        filter_fields = ["title"]

    histogram = ConnectionField(HistogramItemConnection)

    def resolve_histogram(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        edges = []

        last_two_weeks = sorted(self.stats.all(), key=lambda x: x.timestamp)[:14]
        page_info = paginator.get_page_info(len(last_two_weeks))

        for i, day in enumerate(
            last_two_weeks[paginator.slice_from : paginator.slice_to]  # Ignore PEP8Bear
        ):
            edges.append(
                EnvironmentConnection_.Edge(
                    node=HistogramItem(
                        value=day.count, name=day.timestamp.strftime("%d/%m/%Y")
                    ),
                    cursor=paginator.get_edge_cursor(i + 1),
                )
            )

        return HistogramItemConnection(
            page_info=page_info, edges=edges, total_count=len(last_two_weeks)
        )


class SentryStats(graphene.ObjectType):
    weekly_events = graphene.Int()
    weekly_users = graphene.Int()
    issues = DjangoFilterConnectionField(SentryIssue)


class Service(DjangoObjectType):
    repository = graphene.Field(lambda: Repository)
    docs_url = graphene.String()
    pagerduty_info = graphene.Field(lambda: PagerdutyInfo)
    sentry_stats = graphene.Field(lambda: SentryStats)

    environments = DjangoFilterConnectionField(Environment)

    def resolve_pagerduty_info(self, info):
        service_id = self.pagerduty_service_id
        if service_id is None:
            return

        try:
            data = get_oncall_info(service_id)  # Might return django.http.Http404
        except Exception as error:
            log.exception("services.get_oncall_info", error=repr(error))
            return
        return PagerdutyInfo(**data)

    def resolve_sentry_stats(self, info):
        sentry_issues = self.sentry_issues.prefetch_related("stats").all()

        # if not sentry_issues.exists():
        #     return None

        all_sentry_issues = sentry_issues.order_by("-last_seen")
        weekly_stats = all_sentry_issues.calculate_weekly_sentry_stats()

        return SentryStats(
            weekly_events=weekly_stats["events"],
            weekly_users=weekly_stats["users"],
            issues=sentry_issues.problematic(),
        )

    @classmethod
    def from_db(cls, service):
        return cls(
            id=service.id,
            owner=service.owner,
            name=service.name,
            status=service.status,
            impact=service.impact,
            slack_channel=service.slack_channel,
            pagerduty_service=service.pagerduty_service,
            docs_url=service.docs_url,
            repository=service.repository_id,
            all_environments=service.environments,
        )

    class Meta:
        model = services_models.Service
        interfaces = [Node]
        filter_fields = ["name", "owner"]

    def resolve_all_environments(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        edges = []
        filtered_environments = services_models.Environment.objects.filter(
            service_id=self.id
        )
        total = filtered_environments.count()
        page_info = paginator.get_page_info(total)

        for i, issue in enumerate(
            filtered_environments[
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = Environment.from_db(issue)
            edges.append(EnvironmentConnection_.Edge(node=node, cursor=cursor))

        return EnvironmentConnection_(
            page_info=page_info, edges=edges, total_count=total
        )


class Repository(DjangoObjectType, interfaces=[Node]):
    issues = DjangoFilterConnectionField(lambda: Issue)
    dependency_usages = DjangoFilterConnectionField(lambda: DependencyUsage)

    class Meta:
        model = repos_models.Repository
        filter_fields = ["name", "owner"]


class Dependency(DjangoObjectType, interfaces=[Node]):
    dependency_usages = DjangoFilterConnectionField(lambda: DependencyUsage)

    class Meta:
        model = analytics_models.Dependency
        filter_fields = ["name", "type"]

    @classmethod
    def from_db(cls, dependency):
        return cls(id=dependency.id, name=dependency.name, type=dependency.type)

    def resolve_all_dependency_usages(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        filtered_dependency_usages = analytics_models.DependencyUsage.objects.filter(
            dependency_id=self.id
        )
        total = filtered_dependency_usages.count()
        page_info = paginator.get_page_info(total)
        edges = []

        all_dependency_usages_type = self._meta.fields["all_dependency_usages"].type

        for i, dependency_usage in enumerate(
            filtered_dependency_usages[
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = DependencyUsage.from_db(dependency_usage)
            edges.append(all_dependency_usages_type.Edge(node=node, cursor=cursor))

        return all_dependency_usages_type(
            page_info=page_info, edges=edges, total_count=total
        )

    @classmethod
    def get_node(cls, info, id):
        try:
            dependency = analytics_models.Dependency.objects.get(id=id)
            return cls.from_db(dependency)
        except ObjectDoesNotExist:
            return None


class DependencyUsage(DjangoObjectType, interfaces=[Node]):
    dependency = graphene.Field(lambda: Dependency)
    repository = graphene.Field(lambda: Repository)

    class Meta:
        model = analytics_models.DependencyUsage
        filter_fields = ["version"]

    @classmethod
    def from_db(cls, dependency_usage):
        return cls(
            id=dependency_usage.id,
            dependency=dependency_usage.dependency_id,
            repository=dependency_usage.repo_id,
            major_version=dependency_usage.major_version,
            minor_version=dependency_usage.minor_version,
            patch_version=dependency_usage.patch_version,
            for_production=dependency_usage.for_production,
            version=dependency_usage.version,
        )

    @classmethod
    def get_node(cls, info, id):
        try:
            dependency_usage = analytics_models.DependencyUsage.objects.get(id=id)
            return cls.from_db(dependency_usage)
        except ObjectDoesNotExist:
            return None

    def resolve_dependency(self, info):
        return Dependency.from_db(
            analytics_models.Dependency.objects.get(id=self.dependency)
        )

    def resolve_repository(self, info):
        return Repository.from_db(
            repos_models.Repository.objects.get(id=self.repository)
        )


CheckResultStatusEnum = graphene.Enum.from_enum(CheckResultStatus)


class CheckResult(graphene.ObjectType):
    kind_key = graphene.String()
    is_found = graphene.Boolean()
    status = graphene.Field(CheckResultStatusEnum)
    severity = graphene.Field(IssueSeverityEnum)
    effort = graphene.Field(IssueEffortEnum)
    details = JSONString()
    title = graphene.String()
    description = graphene.String()

    class Meta:
        interfaces = [Node]

    @classmethod
    def get_node(cls, info, issue_id):
        try:
            issue = auditing_models.Issue.objects.get(id=issue_id)
            return cls.from_db(issue)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def from_db(cls, issue):
        return cls(
            id=issue.id,
            kind_key=issue.kind_key,
            is_found=issue.is_found,
            details=issue.details,
        )

    @property
    def kind(self):
        return check_discovery.KINDS[self.kind_key]

    def resolve_severity(self, info):
        return self.kind.severity

    def resolve_effort(self, info):
        return self.kind.effort

    def resolve_title(self, info):
        return self.kind.title

    def resolve_description(self, info):
        return self.kind.format_description(self.details)
