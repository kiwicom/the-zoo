# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_wontfix 1'] = {
    'data': {
        'setWontfix': {
            'issue': {
                'comment': 'A good reason',
                'id': 'SXNzdWU6MTA=',
                'status': 'WONTFIX'
            }
        }
    }
}
