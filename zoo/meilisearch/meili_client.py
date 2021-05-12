import meilisearch
from django.conf import settings

meili_client = meilisearch.Client(settings.MEILI_HOST, settings.MEILI_MASTER_KEY)
