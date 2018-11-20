import pytest
from faker import Faker
from zoo.services.models import Service
from zoo.services.forms import ServiceForm
from zoo.repos.models import Repository

pytestmark = pytest.mark.django_db


def test_service_form__basic__correct():
    fake = Faker()
    form = ServiceForm(data={"owner": fake.user_name(), "name": fake.word()})

    assert form.is_valid()
    new_service = form.save()
    assert Service.objects.filter(id=new_service.id).exists()


def test_service_form__basic__incorrect():
    fake = Faker()
    form = ServiceForm(data={"owner": "a" * 101, "name": fake.word()})

    assert not form.is_valid()
    assert form.errors == {
        "owner": ["Ensure this value has at most 100 characters (it has 101)."]
    }


fake = Faker()
service_form_data = {
    "owner": fake.user_name(),
    "name": fake.word(),
    "status": "production",
    "impact": "profit",
    "datacenter": "",
    "slack_channel": "dev-null",
    "repository": "",
    "pagerduty_url": fake.url(),
    "dashboard_url": fake.url(),
    "docs_url": fake.url(),
    "service_url": fake.url(),
    "health_check_url": fake.url(),
}


def test_service_form__complete__correct(repository, data_center):
    form = ServiceForm(
        data={
            **service_form_data,
            "datacenter": data_center.pk,
            "repository": repository.pk,
        }
    )

    assert form.is_valid()


def test_service_form__complete__incorrect_status(repository, data_center):
    form = ServiceForm(
        data={
            **service_form_data,
            "status": "live",
            "datacenter": data_center.pk,
            "repository": repository.pk,
        }
    )

    assert not form.is_valid()
    assert form.errors == {
        "status": ["Select a valid choice. live is not one of the available choices."]
    }


def test_service_form__complete__incorrect_dashboard_url(repository, data_center):
    form = ServiceForm(
        data={
            **service_form_data,
            "dashboard_url": "-",
            "datacenter": data_center.pk,
            "repository": repository.pk,
        }
    )

    assert not form.is_valid()
    assert form.errors == {"dashboard_url": ["Enter a valid URL."]}
