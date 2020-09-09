import pytest
from faker import Faker

from zoo.repos.models import Repository
from zoo.services.forms import ServiceEnvironmentsFormSet, ServiceForm
from zoo.services.models import Service

pytestmark = pytest.mark.django_db


def test_service_form__basic__correct():
    fake = Faker()
    form = ServiceForm(
        data={"owner": fake.user_name(), "name": fake.word(), "exclusions": fake.word()}
    )

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
    "description": fake.sentence(),
    "status": "production",
    "impact": "profit",
    "tier": "",
    "slack_channel": "dev-null",
    "repository": "",
    "pagerduty_service": fake.word(),
    "docs_url": fake.url(),
    "service_url": fake.url(),
    "exclusions": fake.word(),
}


def test_service_form__complete__correct(repository):
    form = ServiceForm(data={**service_form_data, "repository": repository.pk})

    assert form.is_valid()


def test_service_form__exclusions__correct():
    repository = Repository.objects.create(remote_id=1)
    service = Service.objects.create(repository=repository)
    form = ServiceForm(
        instance=service, data={**service_form_data, "repository": repository.pk}
    )
    form.save()
    assert repository.exclusions == service_form_data["exclusions"]


def test_service_form__complete__incorrect_status(repository):
    form = ServiceForm(
        data={**service_form_data, "status": "live", "repository": repository.pk}
    )

    assert not form.is_valid()
    assert form.errors == {
        "status": ["Select a valid choice. live is not one of the available choices."]
    }


service_environments_form__set_data = {
    "environments-TOTAL_FORMS": "2",
    "environments-INITIAL_FORMS": "0",
    "environments-MIN_NUM_FORMS": "2",
    "environments-MAX_NUM_FORMS": "2",
    "environments-0-name": fake.word(),
    "environments-0-healthcheck_url": fake.url(),
    "environments-0-service_urls_0": fake.url(),
    "environments-0-service_urls_1": fake.url(),
    "environments-0-DELETE": False,
    "environments-1-name": fake.word(),
    "environments-1-dashboard_url": fake.url(),
    "environments-1-service_urls_0": fake.url(),
    "environments-1-service_urls_1": fake.url(),
    "environments-1-DELETE": False,
}


def test_service_environment_formset__complete__correct(repository):
    form = ServiceEnvironmentsFormSet(data=service_environments_form__set_data)

    assert form.is_valid()


def test_service_environment_formset__complete__incorrect(repository):
    form = ServiceEnvironmentsFormSet(
        {**service_environments_form__set_data, "environments-0-dashboard_url": "-"}
    )
    assert not form.is_valid()
    assert form.forms[0].errors == {"dashboard_url": ["Enter a valid URL."]}
