# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_unknown_repository 1'] = {
    'data': {
        'checkRepositoryByCommit': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 5,
                    'line': 3
                }
            ],
            'message': 'games/doom is not known to the Zoo.',
            'path': [
                'checkRepositoryByCommit'
            ]
        }
    ]
}

snapshots['test_all_results 1'] = {
    'data': {
        'checkRepositoryByCommit': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 5,
                    'line': 3
                }
            ],
            'message': "type object 'Repository' has no attribute 'from_db'",
            'path': [
                'checkRepositoryByCommit'
            ]
        }
    ]
}

snapshots['test_only_found 1'] = {
    'data': {
        'checkRepositoryByCommit': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 5,
                    'line': 3
                }
            ],
            'message': "type object 'Repository' has no attribute 'from_db'",
            'path': [
                'checkRepositoryByCommit'
            ]
        }
    ]
}

snapshots['test_with_repository 1'] = {
    'data': {
        'checkRepositoryByCommit': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 9,
                    'line': 3
                }
            ],
            'message': "type object 'Repository' has no attribute 'from_db'",
            'path': [
                'checkRepositoryByCommit'
            ]
        }
    ]
}
