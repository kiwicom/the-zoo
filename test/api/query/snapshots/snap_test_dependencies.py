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
            'message': 'Cannot query field "allDependencies" on type "Query". Did you mean "dependencies" or "dependency"?'
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
            'message': 'Cannot query field "allDependencies" on type "Query". Did you mean "dependencies" or "dependency"?'
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
            'message': 'Cannot query field "allDependencies" on type "Query". Did you mean "dependencies" or "dependency"?'
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
            'message': 'Cannot query field "allDependencies" on type "Query". Did you mean "dependencies" or "dependency"?'
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
            'message': 'Cannot query field "allDependencies" on type "Query". Did you mean "dependencies" or "dependency"?'
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
            'message': 'Cannot query field "allDependencies" on type "Query". Did you mean "dependencies" or "dependency"?'
        }
    ]
}

snapshots['test_with_dependency_usage 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 7,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "allDependencies" on type "Query". Did you mean "dependencies" or "dependency"?'
        }
    ]
}

snapshots['test_filter_by_name 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 7,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "allDependencies" on type "Query". Did you mean "dependencies" or "dependency"?'
        }
    ]
}

snapshots['test_filter_by_type 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 7,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "allDependencies" on type "Query". Did you mean "dependencies" or "dependency"?'
        }
    ]
}

snapshots['test_filter_by_type_and_name 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 7,
                    'line': 3
                }
            ],
            'message': 'Cannot query field "allDependencies" on type "Query". Did you mean "dependencies" or "dependency"?'
        }
    ]
}
