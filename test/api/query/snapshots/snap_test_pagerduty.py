# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_pagerduty_service 1'] = {
    'data': {
        'node': {
            'pagerdutyService': {
                'allActiveIncidents': None,
                'htmlUrl': None,
                'id': None,
                'oncallPerson': None,
                'pastWeekTotal': None,
                'summary': None
            }
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 21,
                    'line': 16
                }
            ],
            'message': "'str' object has no attribute 'all_active_incidents'",
            'path': [
                'node',
                'pagerdutyService',
                'allActiveIncidents'
            ]
        }
    ]
}
