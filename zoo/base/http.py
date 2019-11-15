import requests
from django.conf import settings
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


def get_retry_object(retries=5, backoff_factor=0.1):
    """Create an instance of :obj:`urllib3.util.Retry`.

    With default arguments (5 retries with 0.1 backoff factor), urllib3 will sleep
    for 0.0, 0.2, 0.4, 0.8, 1.6 seconds between attempts.
    """
    return Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=(500, 502, 504),
    )


def get_requests_session():
    """Create Python-Request's Session object."""
    session = requests.Session()
    session.headers = {"user-agent": settings.USER_AGENT}
    return session


def requests_retry_session(retries=3, backoff_factor=0.1, session=None):
    """Session which automatically retries requests for 5xx HTTP statuses.

    See https://www.peterbe.com/plog/best-practice-with-retries-with-requests

    Usage example:

    .. code-block:: python

        response = requests_retry_session().get('https://www.peterbe.com/')

        s = requests.Session()
        s.auth = ('user', 'pass')
        s.headers.update({'x-test': 'true'})

        response = requests_retry_session(session=s).get(
            'https://www.peterbe.com'
        )
    """
    session = session or get_requests_session()
    max_retries = get_retry_object(retries=retries, backoff_factor=backoff_factor)
    adapter = HTTPAdapter(max_retries=max_retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


session = requests_retry_session()
