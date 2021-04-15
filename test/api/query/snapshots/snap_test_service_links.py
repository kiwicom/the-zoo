# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_empty 1'] = {
    'data': {
        'allServices': {
            'edges': [
            ],
            'totalCount': 0
        }
    }
}

snapshots['test_all 1'] = {
    'data': {
        'allServices': {
            'edges': [
                {
                    'node': {
                        'allLinks': None
                    }
                }
            ],
            'totalCount': 1
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 13,
                    'line': 7
                }
            ],
            'message': 'Resolved value from the connection field have to be iterable or instance of LinkConnection. Received "None"',
            'path': [
                'allServices',
                'edges',
                0,
                'node',
                'allLinks'
            ]
        }
    ]
}

snapshots['test_first 1'] = {
    'data': {
        'allServices': {
            'edges': [
                {
                    'node': {
                        'allLinks': None
                    }
                }
            ],
            'totalCount': 1
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 13,
                    'line': 7
                }
            ],
            'message': 'Resolved value from the connection field have to be iterable or instance of LinkConnection. Received "None"',
            'path': [
                'allServices',
                'edges',
                0,
                'node',
                'allLinks'
            ]
        }
    ]
}

snapshots['test_last 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 19,
                    'line': 13
                }
            ],
            'message': 'Cannot query field "url" on type "Environment".'
        },
        {
            'locations': [
                {
                    'column': 19,
                    'line': 14
                }
            ],
            'message': 'Cannot query field "icon" on type "Environment".'
        }
    ]
}
