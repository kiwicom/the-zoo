from random import choice, randint

from django.conf import settings

from factory import DjangoModelFactory, Faker, LazyAttribute, SubFactory, Factory
from faker import Faker as OriginalFaker
from zoo.api.models import ApiToken
from zoo.auditing.models import Issue
from zoo.auditing.check_discovery import Kind
from zoo.datacenters.models import InfraNode
from zoo.repos.models import Repository
from zoo.services.models import Service
from zoo.analytics.models import Dependency, DependencyUsage, DependencyType
from zoo.analytics.tasks.repo_analyzers import unpack_version


class RepositoryFactory(DjangoModelFactory):
    class Meta:
        model = Repository

    remote_id = Faker("pyint")
    owner = Faker("user_name")
    name = Faker("domain_word")
    provider = "gitlab"
    url = LazyAttribute(lambda o: f"https://gitlab.com/{o.owner}/{o.name}")


class IssueFactory(DjangoModelFactory):
    class Meta:
        model = Issue

    repository = SubFactory(RepositoryFactory)
    kind_key = LazyAttribute(
        lambda o: "{}:{}".format(
            OriginalFaker().domain_word(), OriginalFaker().domain_word()
        )
    )


class ServiceFactory(DjangoModelFactory):
    class Meta:
        model = Service

    owner = Faker("user_name")
    name = Faker("domain_word")
    impact = choice(["profit", "customers", "customers"])
    repository = SubFactory(RepositoryFactory)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = Faker("user_name")
    email = Faker("email")


class ApiTokenFactory(DjangoModelFactory):
    class Meta:
        model = ApiToken

    purpose = "test"


class DependencyFactory(DjangoModelFactory):
    class Meta:
        model = Dependency

    name = Faker("name")
    type = choice([dtype.value for dtype in DependencyType])


class DependencyUsageFactory(DjangoModelFactory):
    class Meta:
        model = DependencyUsage

    def __init__(self, *args, **kwargs):
        self.version = f"{randint(0,10)}.{randint(0,10)}.{randint(0,10)}"
        unpacked_version = unpack_version(self.version)
        self.major_version = unpacked_version["major_version"]
        self.minor_version = unpacked_version["minor_version"]
        self.patch_version = unpacked_version["patch_version"]

    dependency = SubFactory(DependencyFactory)
    repo = SubFactory(RepositoryFactory)
    for_production = choice(["t", "f"])


class KindFactory(Factory):
    class Meta:
        model = Kind

    namespace = Faker("domain_word")
    category = Faker("domain_word")
    id = Faker("domain_word")
    title = Faker("sentence")
    description = Faker("paragraph")


class InfraNodeFactory(Factory):
    class Meta:
        model = InfraNode

    kind = Faker("domain_word")
    value = Faker("slug")
