import pytest

from zoo.elasticsearch.search import ElasticSearchView

from zoo.services import models as services
from zoo.repos import models as repos

pytestmark = pytest.mark.django_db


ES_RESULT = {'took': 21,
                   'timed_out': False,
                   '_shards': {
                       'total': 7, 'successful': 7, 'skipped': 0, 'failed': 0
                   },
                   'hits': {
                       'total': {
                           'value': 2, 'relation': 'eq'
                       }, 'max_score': 6.4629626,
                       'hits': [
                           {'_index': 'services', '_type': 'service', '_id': '1',
                            '_score': 6.4629626,
                            '_source': {'owner': 'zoo',
                                        'name': 'jungle',
                                        'status': 'discontinued',
                                        'impact': 'impact',
                                        'slack_channel': 'slack channel',
                                        'sentry_project': 'sentry',
                                        'sonarqube_project': 'key',
                                        'rating_grade': None,
                                        'rating_reason': None,
                                        'repository': 1781,
                                        'pagerduty_url': None,
                                        'docs_url': None,
                                        'owner_slug': 'test',
                                        'name_slug': 'test',
                                        'tags': '["general"]'}},
                           {'_index': 'open-api', '_type': 'schema', '_id': 'openapi-gitlab-2',
                            '_score': 0.3955629,
                            '_source': {'title': 'Schema Titler',
                                        'description': 'Description',
                                        'endpoints': [
                                            '/path/{arg}',
                                            '/path',]}}]}}


def test_search_result():
    fake_repo = repos.Repository.objects.create(
        remote_id=2,
        provider='gitlab',
        owner='zoo',
        name='jungle',
        url='http://fake.repo.gitlab.com'
    )
    service = services.Service.objects.create(
        id=1,
        owner='zoo',
        name='jungle',
        repository=fake_repo
    )
    search_class = ElasticSearchView()
    expected_result = {
        'service': [service],
        'service_detail_urls': [service.get_absolute_url()]
    }
    result = search_class._objects_from_result(ES_RESULT)
    assert result == expected_result
