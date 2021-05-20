from unittest.mock import patch

import pytest

from zoo.repos import models as repos
from zoo.services import models as services

pytestmark = pytest.mark.django_db


def test_search_result():
    repo = repos.Repository.objects.create(
        remote_id=2,
        provider="gitlab",
        owner="zoo",
        name="jungle",
        url="http://fake.repo.gitlab.com",
    )
    service = services.Service.objects.create(
        id=1, owner="zoo", name="jungle", repository=repo
    )

    expected_result = {
        "Dependency": [],
        "Service": [service],
        "Schema": [],
    }
    with patch("zoo.globalsearch.views.GlobalSearchView") as mock_view:
        mock_view.get_context_data.return_value = expected_result
        assert expected_result == mock_view.get_context_data()
