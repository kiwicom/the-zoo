import os
from pathlib import Path

import raven
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


def _get_app_version():
    """Return current commit SHA of the app."""
    file_path = Path(__file__)
    for directory in file_path.parents:
        if (directory / ".git").exists():
            return raven.fetch_git_sha(str(directory))

    # if there was no git repo in the parent directories
    return os.getenv("PACKAGE_VERSION")


def requests_retry_session(retries=3, backoff_factor=0.1, session=None):
    """Session which automatically retries requests for 5xx HTTP statuses.

    See https://www.peterbe.com/plog/best-practice-with-retries-with-requests

    Usage example:

    .. code-block:: python

        response = requests_retry_session().get('https://www.peterbe.com/')
        print(response.status_code)

        s = requests.Session()
        s.auth = ('user', 'pass')
        s.headers.update({'x-test': 'true'})

        response = requests_retry_session(session=s).get(
            'https://www.peterbe.com'
        )
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=(500, 502, 504),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


# borrow this file and add some utils here for graphql
