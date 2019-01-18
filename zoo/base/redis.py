from django.conf import settings
from redis import StrictRedis


def get_connection():
    return StrictRedis.from_url(settings.REDIS_CACHE_URL)
