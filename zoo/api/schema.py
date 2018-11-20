import graphene

from . import types
from .mutations import Mutation as ZooMutation
from .query import Query as ZooQuery


class Query(ZooQuery, graphene.ObjectType):
    pass


class Mutation(ZooMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    types=[
        types.CheckResult,
        types.DataCenter,
        types.Dependency,
        types.DependencyUsage,
        types.Issue,
        types.Repository,
        types.Service,
    ],
)
