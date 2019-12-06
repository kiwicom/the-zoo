import pytest

from zoo.datacenters import utils as uut


@pytest.mark.parametrize(
    "email,expected",
    [
        ("jon.doe@kiwi.com", "Jon Doe"),
        ("platform@kiwi.com", "Platform"),
        ("something", "Something"),
    ],
)
def test_email_to_full_name(email, expected):
    assert uut.email_to_full_name(email) == expected
