import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

from ..analytics.models import Dependency, DependencyType, DependencyUsage
from ..auditing.models import Issue
from ..repos.models import Repository
from ..services.models import Service
from . import types
from .paginator import Paginator

DependencyTypeEnum = graphene.Enum.from_enum(DependencyType)


class ServiceType(DjangoObjectType):
    class Meta:
        model = Service


class RepositoryType(DjangoObjectType):
    class Meta:
        model = Repository


class IssueType(DjangoObjectType):
    class Meta:
        model = Issue


class Query(graphene.ObjectType):
    services = graphene.List(ServiceType)
    service = graphene.Field(ServiceType, id=graphene.ID(), name=graphene.String())
    repositories = graphene.List(RepositoryType)
    repository = graphene.Field(
        RepositoryType, id=graphene.ID(), name=graphene.String()
    )
    issues = graphene.List(
        IssueType,
        repository_name=graphene.String(),
        service_name=graphene.String(),
        service_id=graphene.ID(),
    )
    issue = graphene.Field(IssueType, id=graphene.ID())

    def resolve_services(self, info, **kwargs):
        return Service.objects.order_by("name")[:10]

    def resolve_service(self, info, id=None, name=None):
        if id is not None:
            return Service.objects.get(pk=id)
        if name is not None:
            return Service.objects.get(name=name)

    def resolve_repositories(self, info, **kwargs):
        return Repository.objects.all()

    def resolve_repository(self, info, id=None, name=None):
        return Repository.objects.get(pk=id)

    def resolve_issues(
        self, info, repository_name=None, service_id=None, service_name=None
    ):
        if repository_name is not None:
            return Issue.objects.filter(repository__name=repository_name)

        # if repository_name is not None:

    def resolve_issue(
        self, info, id=None,
    ):
        return Issue.objects.get(pk=id)

    node = relay.Node.Field()
    all_issues = relay.ConnectionField(
        types.IssueConnection,
        description="List of issues. Returns first 10 nodes if pagination is not specified.",
    )
    all_services = relay.ConnectionField(
        types.ServiceConnection,
        description="List of services. Returns first 10 nodes if pagination is not specified.",
    )
    all_repositories = relay.ConnectionField(
        types.RepositoryConnection,
        description="List of repositories. Returns first 10 nodes if pagination is not specified.",
    )
    all_dependencies = relay.ConnectionField(
        types.DependencyConnection,
        dependency_type=DependencyTypeEnum(),
        name=graphene.String(),
        description="List of dependency usages. Returns first 10 nodes if pagination is not specified.",
    )
    all_dependency_usages = relay.ConnectionField(
        types.DependencyUsageConnection,
        description="List of dependency usages. Returns first 10 nodes if pagination is not specified.",
    )

    def resolve_all_issues(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        total = Issue.objects.all().count()
        page_info = paginator.get_page_info(total)
        edges = []

        for i, issue in enumerate(
            Issue.objects.all()[
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = types.Issue.from_db(issue)
            edges.append(types.IssueConnection.Edge(node=node, cursor=cursor))

        return types.IssueConnection(
            page_info=page_info, edges=edges, total_count=total
        )

    def resolve_all_services(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        total = Service.objects.all().count()
        page_info = paginator.get_page_info(total)
        edges = []

        for i, service in enumerate(
            Service.objects.all()[
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = types.Service.from_db(service)
            edges.append(types.ServiceConnection.Edge(node=node, cursor=cursor))

        return types.ServiceConnection(
            page_info=page_info, edges=edges, total_count=total
        )

    def resolve_all_repositories(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        total = Repository.objects.all().count()
        page_info = paginator.get_page_info(total)
        edges = []

        for i, repo in enumerate(
            Repository.objects.all()[
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = types.Repository.from_db(repo)
            edges.append(types.RepositoryConnection.Edge(node=node, cursor=cursor))

        return types.RepositoryConnection(
            page_info=page_info, edges=edges, total_count=total
        )

    def resolve_all_dependencies(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        filtered_dependencies = Dependency.objects.all()

        if "name" in kwargs:
            filtered_dependencies = filtered_dependencies.filter(
                name__icontains=kwargs["name"]
            )

        if "dependency_type" in kwargs:
            filtered_dependencies = filtered_dependencies.filter(
                type=kwargs["dependency_type"]
            )

        total = filtered_dependencies.count()
        page_info = paginator.get_page_info(total)
        edges = []

        for i, dependency in enumerate(
            filtered_dependencies[
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = types.Dependency.from_db(dependency)
            edges.append(types.DependencyConnection.Edge(node=node, cursor=cursor))

        return types.DependencyConnection(
            page_info=page_info, edges=edges, total_count=total
        )

    def resolve_all_dependency_usages(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        total = DependencyUsage.objects.all().count()
        page_info = paginator.get_page_info(total)
        edges = []

        for i, dependency_usage in enumerate(
            DependencyUsage.objects.all()[
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = types.DependencyUsage.from_db(dependency_usage)
            edges.append(types.DependencyUsageConnection.Edge(node=node, cursor=cursor))

        return types.DependencyUsageConnection(
            page_info=page_info, edges=edges, total_count=total
        )
