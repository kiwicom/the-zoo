from django.conf import settings
from redis import StrictRedis
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(wait=wait_exponential(multiplier=1, min=1, max=5), stop=stop_after_attempt(5))
def get_connection(**kwargs):
    return StrictRedis.from_url(settings.REDIS_CACHE_URL, **kwargs)
