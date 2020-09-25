# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_empty 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 7,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "allIssues" on type "Query".'
        }
    ]
}

snapshots['test_all 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 7,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "allIssues" on type "Query".'
        }
    ]
}

snapshots['test_first 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 7,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "allIssues" on type "Query".'
        }
    ]
}

snapshots['test_first_after 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 7,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "allIssues" on type "Query".'
        }
    ]
}

snapshots['test_last_before 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 7,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "allIssues" on type "Query".'
        }
    ]
}

snapshots['test_with_repository 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 7,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "allIssues" on type "Query".'
        }
    ]
}

snapshots['test_last 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 7,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "allIssues" on type "Query".'
        }
    ]
}
