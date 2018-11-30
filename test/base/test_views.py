import pytest

pytestmark = pytest.mark.django_db


def test_robots_txt(client, snapshot):
    response = client.get("/robots.txt")
    assert response.status_code == 200
    snapshot.assert_match(response.content)


def test_ping(client, snapshot):
    response = client.get("/ping")
    assert response.status_code == 200
    snapshot.assert_match(response.content)
