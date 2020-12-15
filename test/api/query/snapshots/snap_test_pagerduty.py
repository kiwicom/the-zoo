# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_pagerduty_service 1'] = {
    'data': {
        'node': {
            'pagerdutyInfo': {
                'allActiveIncidents': {
                    'edges': [
                        {
                            'node': {
                                'createdAt': '2020-04-28T11:39:52Z',
                                'description': 'incident_description',
                                'htmlUrl': 'https://example.com/incidents/1',
                                'id': 'INCIDENT1',
                                'status': 'triggered',
                                'summary': 'incident_summary'
                            }
                        }
                    ],
                    'totalCount': 1
                },
                'htmlUrl': 'https://example.com/service/1',
                'id': '1A2B3',
                'oncallPerson': {
                    'htmlUrl': 'https://example.com/users/1',
                    'id': 'USER1',
                    'summary': 'user_summary',
                    'type': 'user'
                },
                'pastWeekTotal': 2,
                'summary': 'service_sumary'
            }
        }
    }
}
