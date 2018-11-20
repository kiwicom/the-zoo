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

snapshots['test_datacenter 1'] = {
    'data': {
        'node': {
            'id': 'RGF0YUNlbnRlcjoxMA==',
            'provider': 'kiwi',
            'region': 'Oklahoma'
        }
    }
}

snapshots['test_service 1'] = {
    'data': {
        'node': {
            'dashboardUrl': 'https://dashboard/skypicker/sale/',
            'docsUrl': 'https://docs/skypicker/docs/',
            'healthCheckUrl': 'https://skypicekr/health',
            'id': 'U2VydmljZToxMA==',
            'impact': 'sales',
            'name': 'allen-nobles',
            'owner': 'bradltwat',
            'pagerdutyUrl': 'https://pagerduty/sales/',
            'slackChannel': 'https://gitlab.slack',
            'status': 'fixed'
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
            'lastCheck': '2018-08-22 11:36:48+00:00',
            'remoteIssueId': 234,
            'status': 'new'
        }
    }
}

snapshots['test_dependency_usage 1'] = {
    'data': {
        'node': {
            'forProduction': 'false',
            'id': 'RGVwZW5kZW5jeVVzYWdlOjEw',
            'majorVersion': 3,
            'minorVersion': 2,
            'patchVersion': 4,
            'version': '3.2.4'
        }
    }
}

snapshots['test_dependency 1'] = {
    'data': {
        'node': {
            'id': 'RGVwZW5kZW5jeToxMA==',
            'name': 'python',
            'type': 'Language'
        }
    }
}
