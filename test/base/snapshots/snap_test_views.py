# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['test_robots_txt 1'] = b'User-agent: *\nDisallow: /'

snapshots['test_ping 1'] = b'200 Pong'
