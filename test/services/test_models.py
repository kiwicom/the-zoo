import pytest

from zoo.services import models as uut

pytestmark = pytest.mark.django_db


def test_service_absolute_url():
    service = uut.Service.objects.create(pk=1, owner="jozo", name="gin")
    assert service.get_absolute_url() == "/services/jozo/gin"
