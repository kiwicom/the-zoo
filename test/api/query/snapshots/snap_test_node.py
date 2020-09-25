# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_repository 1'] = {
    'data': {
        'node': {
            'id': 'UmVwb3NpdG9yeToxMA==',
            'name': 'james-rivera',
            'owner': 'sharon54',
            'remoteId': 2783,
            'url': 'https://gitlab.com/sharon54/jones-rivera'
        }
    }
}

snapshots['test_issue 1'] = {
    'data': {
        'node': {
            'comment': 'Mars',
            'details': '{"lunch": "good", "money": true, "balance": 0}',
            'id': 'SXNzdWU6MTA=',
            'kindKey': 'harris:reyes',
            'lastCheck': '2018-08-22T11:36:48+00:00',
            'remoteIssueId': 234,
            'status': 'NEW'
        }
    }
}

snapshots['test_dependency_usage 1'] = {
    'data': {
        'node': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 13,
                    'line': 5
                }
            ],
            'message': "'DependencyUsage' object has no attribute 'pk'",
            'path': [
                'node',
                'id'
            ]
        }
    ]
}

snapshots['test_dependency 1'] = {
    'data': {
        'node': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 13,
                    'line': 5
                }
            ],
            'message': "'Dependency' object has no attribute 'pk'",
            'path': [
                'node',
                'id'
            ]
        }
    ]
}

snapshots['test_service 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 11
                }
            ],
            'message': 'Field "pagerdutyService" of type "PagerdutyService" must have a sub selection.'
        }
    ]
}
