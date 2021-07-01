import pytest
import yaml

from zoo.repos.entities_yaml import generate, validate
from zoo.repos.models import Repository
from zoo.services.models import Environment, Service

pytestmark = pytest.mark.django_db


@pytest.fixture
def generate_base_component(base_component_factory, link_factory, group_factory):
    group = group_factory(id=1, product_owner="john", project_owner="doe")
    group.save()
    component = base_component_factory(
        id=1,
        name="base",
        type="database",
        description="This is my fancy component",
        kind="component",
        owner="platform",
        service=None,
        library=None,
        source__id=1,
        source__remote_id=1,
        source__owner="jasckson",
        source__name="thiwer",
        source__url="https://gitlab.com/thiwer/thiwer",
        group=group,
    )
    component.save()
    link_factory(
        id=1,
        name="Datadog",
        url="https://dashboard.datadog.com",
        icon="poop",
        component=component,
    )
    link_factory(
        id=2,
        name="Sentry",
        url="https://sentry.skypicker.com",
        component=component,
    )


def test_generate_base_component(generate_base_component):
    expected = """
- apiVersion: v1alpha1
  kind: component
  metadata:
    name: base
    owner: platform
    group:
      product_owner: john
      project_owner: doe
      maintainers: []
    description: This is my fancy component
    tags: []
    links:
    - name: Datadog
      url: https://dashboard.datadog.com
      icon: poop
    - name: Sentry
      url: https://sentry.skypicker.com
      icon: null
  spec:
    type: database
"""
    repository = Repository.objects.get(pk=1)
    content = generate(repository)
    assert validate(content)
    assert expected.strip() == content.strip()
