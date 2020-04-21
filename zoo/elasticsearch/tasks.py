from celery import shared_task

from zoo.elasticsearch.indexer import Indexer


@shared_task
def index_documents():
    indexer = Indexer()
    indexer.index_specified_models()
