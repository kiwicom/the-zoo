import time

import pytest

from zoo.analytics.models import Dependency, DependencyType
from zoo.globalsearch.indexer import Indexer as uut
from zoo.services.models import Service

pytestmark = pytest.mark.django_db


def _initialize(client, models):
    for model, index in models:
        client.create_index(uid=index, options={"primaryKey": "id"})


def test_index_model():
    Service(owner="test", name="test").save()
    Dependency(name="test", type=DependencyType.LANG).save()

    indexer = uut()
    _initialize(indexer.meiliclient, indexer.models_to_index)

    indexer.index_specified_models()

    time.sleep(1)  # Sometimes indexing isn't ready for us to search :/

    for model, index in indexer.models_to_index:
        hits = indexer.meiliclient.get_index(index).search("test")["hits"]
        assert model.objects.filter(name="test").first().pk == hits[0]["id"]
