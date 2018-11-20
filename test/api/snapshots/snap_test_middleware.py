# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_no_auth_header 1'] = b'Missing Authorization header for API.'

snapshots['test_wrong_auth_header 1'] = b"Wrong Authorization header value. Expected: 'Bearer <token>'"

snapshots['test_invalid_token 1'] = b'401: Unauthorized'
