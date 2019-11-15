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
        'checkRepositoryByCommit': {
            'allCheckResults': [
                {
                    'description': 'Description for A:new | Status: new -> known',
                    'details': '{"was": "new", "is": "known"}',
                    'effort': 'UNDEFINED',
                    'isFound': True,
                    'kindKey': 'A:new',
                    'severity': 'UNDEFINED',
                    'status': 'KNOWN',
                    'title': 'Title for A:new'
                },
                {
                    'description': 'Description for A:fixed | Status: fixed -> reopened',
                    'details': '{"was": "fixed", "is": "reopened"}',
                    'effort': 'LOW',
                    'isFound': True,
                    'kindKey': 'A:fixed',
                    'severity': 'ADVICE',
                    'status': 'REOPENED',
                    'title': 'Title for A:fixed'
                },
                {
                    'description': 'Description for A:wontfix | Status: wontfix -> wontfix',
                    'details': '{"was": "wontfix", "is": "wontfix"}',
                    'effort': 'MEDIUM',
                    'isFound': True,
                    'kindKey': 'A:wontfix',
                    'severity': 'WARNING',
                    'status': 'WONTFIX',
                    'title': 'Title for A:wontfix'
                },
                {
                    'description': 'Description for A:not-found | Status: not-found -> new',
                    'details': '{"was": "not-found", "is": "new"}',
                    'effort': 'HIGH',
                    'isFound': True,
                    'kindKey': 'A:not-found',
                    'severity': 'CRITICAL',
                    'status': 'NEW',
                    'title': 'Title for A:not-found'
                },
                {
                    'description': 'Description for A:reopened | Status: reopened -> known',
                    'details': '{"was": "reopened", "is": "known"}',
                    'effort': 'UNDEFINED',
                    'isFound': True,
                    'kindKey': 'A:reopened',
                    'severity': 'UNDEFINED',
                    'status': 'KNOWN',
                    'title': 'Title for A:reopened'
                },
                {
                    'description': 'Description for B:new | Status: new -> fixed',
                    'details': '{"was": "new", "is": "fixed"}',
                    'effort': 'LOW',
                    'isFound': False,
                    'kindKey': 'B:new',
                    'severity': 'ADVICE',
                    'status': 'FIXED',
                    'title': 'Title for B:new'
                },
                {
                    'description': 'Description for B:fixed | Status: fixed -> not-found',
                    'details': '{"was": "fixed", "is": "not-found"}',
                    'effort': 'MEDIUM',
                    'isFound': False,
                    'kindKey': 'B:fixed',
                    'severity': 'WARNING',
                    'status': 'NOT_FOUND',
                    'title': 'Title for B:fixed'
                },
                {
                    'description': 'Description for B:wontfix | Status: wontfix -> fixed',
                    'details': '{"was": "wontfix", "is": "fixed"}',
                    'effort': 'HIGH',
                    'isFound': False,
                    'kindKey': 'B:wontfix',
                    'severity': 'CRITICAL',
                    'status': 'FIXED',
                    'title': 'Title for B:wontfix'
                },
                {
                    'description': 'Description for B:not-found | Status: not-found -> not-found',
                    'details': '{"was": "not-found", "is": "not-found"}',
                    'effort': 'LOW',
                    'isFound': False,
                    'kindKey': 'B:not-found',
                    'severity': 'ADVICE',
                    'status': 'NOT_FOUND',
                    'title': 'Title for B:not-found'
                },
                {
                    'description': 'Description for B:reopened | Status: reopened -> fixed',
                    'details': '{"was": "reopened", "is": "fixed"}',
                    'effort': 'HIGH',
                    'isFound': False,
                    'kindKey': 'B:reopened',
                    'severity': 'UNDEFINED',
                    'status': 'FIXED',
                    'title': 'Title for B:reopened'
                },
                {
                    'description': 'Description for C:is-found | Status:  -> ',
                    'details': None,
                    'effort': 'HIGH',
                    'isFound': True,
                    'kindKey': 'C:is-found',
                    'severity': 'CRITICAL',
                    'status': 'NEW',
                    'title': 'Title for C:is-found'
                },
                {
                    'description': 'Description for C:not-found | Status:  -> ',
                    'details': None,
                    'effort': 'LOW',
                    'isFound': False,
                    'kindKey': 'C:not-found',
                    'severity': 'WARNING',
                    'status': 'NOT_FOUND',
                    'title': 'Title for C:not-found'
                }
            ]
        }
    }
}

snapshots['test_only_found 1'] = {
    'data': {
        'checkRepositoryByCommit': {
            'allCheckResults': [
                {
                    'description': 'Description for A:new | Status: new -> known',
                    'details': '{"was": "new", "is": "known"}',
                    'effort': 'UNDEFINED',
                    'isFound': True,
                    'kindKey': 'A:new',
                    'severity': 'UNDEFINED',
                    'status': 'KNOWN',
                    'title': 'Title for A:new'
                },
                {
                    'description': 'Description for A:fixed | Status: fixed -> reopened',
                    'details': '{"was": "fixed", "is": "reopened"}',
                    'effort': 'LOW',
                    'isFound': True,
                    'kindKey': 'A:fixed',
                    'severity': 'ADVICE',
                    'status': 'REOPENED',
                    'title': 'Title for A:fixed'
                },
                {
                    'description': 'Description for A:wontfix | Status: wontfix -> wontfix',
                    'details': '{"was": "wontfix", "is": "wontfix"}',
                    'effort': 'MEDIUM',
                    'isFound': True,
                    'kindKey': 'A:wontfix',
                    'severity': 'WARNING',
                    'status': 'WONTFIX',
                    'title': 'Title for A:wontfix'
                },
                {
                    'description': 'Description for A:not-found | Status: not-found -> new',
                    'details': '{"was": "not-found", "is": "new"}',
                    'effort': 'HIGH',
                    'isFound': True,
                    'kindKey': 'A:not-found',
                    'severity': 'CRITICAL',
                    'status': 'NEW',
                    'title': 'Title for A:not-found'
                },
                {
                    'description': 'Description for A:reopened | Status: reopened -> known',
                    'details': '{"was": "reopened", "is": "known"}',
                    'effort': 'UNDEFINED',
                    'isFound': True,
                    'kindKey': 'A:reopened',
                    'severity': 'UNDEFINED',
                    'status': 'KNOWN',
                    'title': 'Title for A:reopened'
                },
                {
                    'description': 'Description for C:is-found | Status:  -> ',
                    'details': None,
                    'effort': 'HIGH',
                    'isFound': True,
                    'kindKey': 'C:is-found',
                    'severity': 'CRITICAL',
                    'status': 'NEW',
                    'title': 'Title for C:is-found'
                }
            ]
        }
    }
}

snapshots['test_with_repository 1'] = {
    'data': {
        'checkRepositoryByCommit': {
            'repository': {
                'id': 'UmVwb3NpdG9yeTo0Mg==',
                'name': 'lemmings',
                'owner': 'games',
                'remoteId': 3,
                'url': 'https://gitlab.com/games/lemmings'
            }
        }
    }
}
