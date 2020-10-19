from celery import shared_task

from zoo.meilisearch.indexer import Indexer


@shared_task
def index_db_model_instances():
    indexer = Indexer()
    indexer.index_specified_models()


@shared_task
def index_openapi_definitions():
    indexer = Indexer()
    indexer.index_openapi()
