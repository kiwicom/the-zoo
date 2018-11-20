import arrow
import pytest

from django.db.utils import IntegrityError

from zoo.api import models as uut

pytestmark = pytest.mark.django_db


def test_api_token__create_without_purpose():
    with pytest.raises(IntegrityError):
        uut.ApiToken.objects.create()


def test_api_token__create(freezer):
    token = uut.ApiToken.objects.create(purpose="test token")
    assert token.created_at == arrow.utcnow().datetime
    assert len(token.token) > 20
    # check that tokens are generated randomly
    token2 = uut.ApiToken.objects.create(purpose="test token 2")
    assert token.token != token2.token
