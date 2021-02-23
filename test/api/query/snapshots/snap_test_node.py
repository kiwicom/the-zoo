# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_dependency 1'] = {
    'data': {
        'node': {
            'id': 'RGVwZW5kZW5jeToxMA==',
            'name': 'python',
            'type': 'LANGUAGE'
        }
    }
}

snapshots['test_dependency_usage 1'] = {
    'data': {
        'node': {
            'forProduction': False,
            'id': 'RGVwZW5kZW5jeVVzYWdlOjEw',
            'majorVersion': 3,
            'minorVersion': 2,
            'patchVersion': 4,
            'version': '3.2.4'
        }
    }
}

snapshots['test_issue 1'] = {
    'data': {
        'node': {
            'comment': 'Mars',
            'details': '{"lunch": "good", "money": true, "balance": 0}',
            'id': 'SXNzdWU6MTA=',
            'kind': {
                'category': 'deleted',
                'description': 'This issue has been deleted so there is no description available for it.',
                'effort': 'undefined',
                'id': 'ZGVsZXRlZDpkZWxldGVk',
                'key': 'deleted:deleted',
                'namespace': 'deleted',
                'patch': 'deleted',
                'severity': 'undefined',
                'title': '[deleted issue]'
            },
            'kindKey': 'harris:reyes',
            'lastCheck': '2018-08-22T11:36:48+00:00',
            'patchPreview': '''


  <div class="ui info message">No auto-generated patches can be applied.</div>

''',
            'remoteIssueId': 234,
            'remoteIssueUrl': 'https://gitlab.com/bakerkristine/hickman/issues/234',
            'status': 'NEW'
        }
    }
}

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

snapshots['test_service 1'] = {
    'data': {
        'node': {
            'docsUrl': 'https://docs/skypicker/docs/',
            'id': 'U2VydmljZToxMA==',
            'impact': 'PROFIT',
            'name': 'allen-nobles',
            'owner': 'bradltwat',
            'pagerdutyInfo': None,
            'slackChannel': 'https://gitlab.slack',
            'status': 'BETA'
        }
    }
}
