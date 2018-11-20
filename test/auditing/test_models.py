import textwrap

import pytest
from zoo.auditing import models as uut
from zoo.auditing.check_discovery import Kind


pytestmark = pytest.mark.django_db


def test_issue_description_html(repository, monkeypatch):
    TEMPLATED_KIND = Kind(
        namespace="py_requirements",
        category="Python Requirements",
        id="use_pip_compile",
        title="YUse pip-compile to generate your requirements",
        description=textwrap.dedent(
            """
            To keep package versions neat and tidy, we normally use [pip-tools](https://github.com/jazzband/pip-tools
            ). And you should, too!
            """
        ).strip(),
    )
    monkeypatch.setitem(uut.KINDS, TEMPLATED_KIND.key, TEMPLATED_KIND)

    issue = uut.Issue.objects.create(
        repository=repository, kind_key="py_requirements:use_pip_compile"
    )

    assert "<p>" in issue.description_html, "description is not rendered at all"
    assert "pip-tools" in issue.description_html, "description text is missing"
