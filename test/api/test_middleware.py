from unittest.mock import Mock

import pytest

from zoo.api import middleware as uut
from zoo.api.models import ApiToken

pytestmark = pytest.mark.django_db


def test_not_api_url(settings):
    settings.ZOO_API_URL = r"^/graphql$"
    request = Mock(path="/admin")

    middleware = uut.ApiTokenAuthenticationMiddleware(lambda r: r)
    response = middleware(request)

    assert response == request


def test_user_is_authenticated(settings):
    settings.ZOO_API_URL = r"^/graphql$"
    request = Mock(**{"path": "/admin", "user.is_authenticated": True})

    middleware = uut.ApiTokenAuthenticationMiddleware(lambda r: r)
    response = middleware(request)

    assert response == request


def test_no_auth_header(settings, snapshot):
    settings.ZOO_API_URL = r"^/graphql$"
    request = Mock(
        **{
            "path": "/graphql",
            "user.is_authenticated": False,
            "META.get.return_value": None,
        }
    )

    middleware = uut.ApiTokenAuthenticationMiddleware(lambda r: r)
    response = middleware(request)

    request.META.get.assert_called_once_with("HTTP_AUTHORIZATION")
    assert response.status_code == 401
    snapshot.assert_match(response.content)


def test_wrong_auth_header(settings, snapshot):
    settings.ZOO_API_URL = r"^/graphql$"
    request = Mock(
        **{
            "path": "/graphql",
            "user.is_authenticated": False,
            "META.get.return_value": "Token IDKFA",
        }
    )

    middleware = uut.ApiTokenAuthenticationMiddleware(lambda r: r)
    response = middleware(request)

    request.META.get.assert_called_once_with("HTTP_AUTHORIZATION")
    assert response.status_code == 401
    snapshot.assert_match(response.content)


def test_invalid_token(settings, snapshot):
    settings.ZOO_API_URL = r"^/graphql$"
    request = Mock(
        **{
            "path": "/graphql",
            "user.is_authenticated": False,
            "META.get.return_value": "Bearer IDDQD",
        }
    )

    middleware = uut.ApiTokenAuthenticationMiddleware(lambda r: r)
    response = middleware(request)

    request.META.get.assert_called_once_with("HTTP_AUTHORIZATION")
    assert response.status_code == 401
    snapshot.assert_match(response.content)


def test_valid_token(settings, snapshot, api_token):
    settings.ZOO_API_URL = r"^/graphql$"
    request = Mock(
        **{
            "path": "/graphql",
            "user.is_authenticated": False,
            "META.get.return_value": "Bearer {}".format(api_token.token),
        }
    )

    middleware = uut.ApiTokenAuthenticationMiddleware(lambda r: r)
    response = middleware(request)

    request.META.get.assert_called_once_with("HTTP_AUTHORIZATION")
    assert response == request
