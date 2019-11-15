import json
import os
import tarfile
from pathlib import Path

import pytest
import testing.postgresql
from django.db import connections
from environ import Env
from faker import Faker
from pytest_factoryboy import register

from zoo.auditing.runner import CheckContext

from . import dummy
from .factories import (
    ApiTokenFactory,
    DependencyFactory,
    DependencyUsageFactory,
    EnvironmentFactory,
    InfraNodeFactory,
    IssueFactory,
    KindFactory,
    RepositoryFactory,
    ServiceFactory,
    UserFactory,
)

register(ApiTokenFactory)
register(RepositoryFactory)
register(IssueFactory)
register(UserFactory)
register(ServiceFactory)
register(EnvironmentFactory)
register(DependencyFactory)
register(DependencyUsageFactory)
register(KindFactory)
register(InfraNodeFactory)


fake = Faker()


@pytest.fixture(scope="session")
def db_url():
    try:
        yield os.environ["TEST_DATABASE_URL"]

    except KeyError:
        with testing.postgresql.Postgresql() as db:
            yield db.url()


@pytest.fixture(scope="session")
def django_db_modify_db_settings(db_url):
    from django.conf import settings

    settings.DATABASES["default"] = Env.db_url_config(db_url)
    del connections["default"]  # have Django recreate the connection later


@pytest.fixture
def fake_dir(tmpdir):
    return tmpdir.mkdir(fake.pystr())


@pytest.fixture
def fake_path(fake_dir):
    return Path(fake_dir.dirname)


@pytest.fixture
def repo_archive(tmpdir):
    tmp = Path(tmpdir) / fake.pystr()
    tmp.mkdir()
    archive = tmp / "repo.tar"
    with tarfile.open(archive, "w") as tar:
        inner_folder = tmp / fake.pystr()
        inner_folder.mkdir()
        for name, content in dummy.repo_files.items():
            file = inner_folder / name
            file.write_text(content)
        tar.add(inner_folder)
    archive_file_object = archive.open("rb")
    yield archive_file_object
    archive_file_object.close()


@pytest.fixture
def check_context(repository, fake_path):
    return CheckContext(repository, fake_path)


@pytest.fixture(scope="session")
def check_factory():
    def factory(kind_key, is_found, details=None):
        def check(context):
            yield context.Result(kind_key, is_found, details)

        return check

    return factory


@pytest.fixture
def call_api(client, api_token):
    def _call_api(query, input=None):
        variables = json.dumps({"input": input or {}})
        res = client.post(
            "/graphql",
            {"query": query, "variables": variables},
            HTTP_AUTHORIZATION=f"Bearer {api_token.token}",
        )
        return res.json()

    return _call_api
