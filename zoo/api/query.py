import graphene
from graphene.relay import Node
from graphene_django.filter import DjangoFilterConnectionField

from ..analytics.models import DependencyType
from . import types

DependencyTypeEnum = graphene.Enum.from_enum(DependencyType)


class Query(graphene.ObjectType):
    node = Node.Field()

    service = Node.Field(types.Service)
    services = DjangoFilterConnectionField(
        types.Service,
        description="List of services. Returns at most 100 nodes if pagination is not specified.",
    )

    repository = Node.Field(types.Repository)
    repositories = DjangoFilterConnectionField(
        types.Repository,
        description="List of repositories. Returns at most 100 nodes if pagination is not specified.",
    )

    dependency = Node.Field(types.Dependency)
    dependencies = DjangoFilterConnectionField(
        types.Dependency,
        description="List of dependency usages. Returns at most 100 nodes if pagination is not specified.",
    )

    dependency_usage = Node.Field(types.DependencyUsage)
    dependency_usages = DjangoFilterConnectionField(
        types.DependencyUsage,
        description="List of dependency usages. Returns at most 100 nodes if pagination is not specified.",
    )
