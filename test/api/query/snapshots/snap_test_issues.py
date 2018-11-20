# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_empty 1'] = {
    'data': {
        'allIssues': {
            'edges': [
            ],
            'pageInfo': {
                'endCursor': None,
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': None
            },
            'totalCount': 0
        }
    }
}

snapshots['test_all 1'] = {
    'data': {
        'allIssues': {
            'edges': [
                {
                    'node': {
                        'comment': 'Saturn',
                        'details': '{"I": true, "data": "restored"}',
                        'id': 'SXNzdWU6MQ==',
                        'kindKey': 'moran:alex',
                        'lastCheck': '2018-09-03 13:09:21.022164+00:00',
                        'remoteIssueId': 62,
                        'status': 'new'
                    }
                },
                {
                    'node': {
                        'comment': 'Juno',
                        'details': '{"data": "restored", "need": true}',
                        'id': 'SXNzdWU6Mg==',
                        'kindKey': 'cook:alice',
                        'lastCheck': '2018-09-03 13:09:21.022164+00:00',
                        'remoteIssueId': 636,
                        'status': 'new'
                    }
                },
                {
                    'node': {
                        'comment': 'Jupiter',
                        'details': '{"data": "restored", "more": true}',
                        'id': 'SXNzdWU6Mw==',
                        'kindKey': 'pride-moran:john',
                        'lastCheck': '2018-09-03 13:09:21.022164+00:00',
                        'remoteIssueId': 6346,
                        'status': 'new'
                    }
                },
                {
                    'node': {
                        'comment': 'Herse',
                        'details': '{"data": "restored", "power": true}',
                        'id': 'SXNzdWU6NA==',
                        'kindKey': 'denis:roman',
                        'lastCheck': '2018-09-03 13:09:21.022164+00:00',
                        'remoteIssueId': 9346,
                        'status': 'new'
                    }
                },
                {
                    'node': {
                        'comment': 'Pluto',
                        'details': '{"data": "restored", "now!": true}',
                        'id': 'SXNzdWU6NQ==',
                        'kindKey': 'dennis:moran',
                        'lastCheck': '2018-09-03 13:09:21.022164+00:00',
                        'remoteIssueId': 65,
                        'status': 'new'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'NQ==',
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': 'MQ=='
            },
            'totalCount': 5
        }
    }
}

snapshots['test_first 1'] = {
    'data': {
        'allIssues': {
            'edges': [
                {
                    'node': {
                        'comment': 'Saturn',
                        'details': '{"I": true, "data": "restored"}',
                        'id': 'SXNzdWU6MQ==',
                        'kindKey': 'moran:alex',
                        'lastCheck': '2018-09-03 13:09:21.022164+00:00',
                        'remoteIssueId': 62,
                        'status': 'new'
                    }
                },
                {
                    'node': {
                        'comment': 'Juno',
                        'details': '{"data": "restored", "need": true}',
                        'id': 'SXNzdWU6Mg==',
                        'kindKey': 'cook:alice',
                        'lastCheck': '2018-09-03 13:09:21.022164+00:00',
                        'remoteIssueId': 636,
                        'status': 'new'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'Mg==',
                'hasNextPage': True,
                'hasPreviousPage': False,
                'startCursor': 'MQ=='
            },
            'totalCount': 5
        }
    }
}

snapshots['test_first_after 1'] = {
    'data': {
        'allIssues': {
            'edges': [
                {
                    'node': {
                        'comment': 'Juno',
                        'details': '{"data": "restored", "need": true}',
                        'id': 'SXNzdWU6Mg==',
                        'kindKey': 'cook:alice',
                        'lastCheck': '2018-09-03 13:09:21.022164+00:00',
                        'remoteIssueId': 636,
                        'status': 'new'
                    }
                },
                {
                    'node': {
                        'comment': 'Jupiter',
                        'details': '{"data": "restored", "more": true}',
                        'id': 'SXNzdWU6Mw==',
                        'kindKey': 'pride-moran:john',
                        'lastCheck': '2018-09-03 13:09:21.022164+00:00',
                        'remoteIssueId': 6346,
                        'status': 'new'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'Mw==',
                'hasNextPage': True,
                'hasPreviousPage': True,
                'startCursor': 'Mg=='
            },
            'totalCount': 5
        }
    }
}

snapshots['test_last_before 1'] = {
    'data': {
        'allIssues': {
            'edges': [
                {
                    'node': {
                        'comment': 'Saturn',
                        'details': '{"I": true, "data": "restored"}',
                        'id': 'SXNzdWU6MQ==',
                        'kindKey': 'moran:alex',
                        'lastCheck': '2018-09-03 13:09:21.022164+00:00',
                        'remoteIssueId': 62,
                        'status': 'new'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'MQ==',
                'hasNextPage': True,
                'hasPreviousPage': False,
                'startCursor': 'MQ=='
            },
            'totalCount': 5
        }
    }
}

snapshots['test_with_repository 1'] = {
    'data': {
        'allIssues': {
            'edges': [
                {
                    'node': {
                        'comment': 'Saturn',
                        'details': '{"I": true, "data": "restored"}',
                        'id': 'SXNzdWU6MQ==',
                        'kindKey': 'moran:alex',
                        'lastCheck': '2018-09-03 13:09:21.022164+00:00',
                        'remoteIssueId': 62,
                        'repository': {
                            'id': 'UmVwb3NpdG9yeTozNg==',
                            'name': 'blumed',
                            'owner': 'john',
                            'remoteId': 234,
                            'url': 'https://home.com/url'
                        },
                        'status': 'new'
                    }
                },
                {
                    'node': {
                        'comment': 'Juno',
                        'details': '{"data": "restored", "need": true}',
                        'id': 'SXNzdWU6Mg==',
                        'kindKey': 'cook:alice',
                        'lastCheck': '2018-09-03 13:09:21.022164+00:00',
                        'remoteIssueId': 636,
                        'repository': {
                            'id': 'UmVwb3NpdG9yeTozNw==',
                            'name': 'fisher',
                            'owner': 'john',
                            'remoteId': 754,
                            'url': 'https://home.com/url'
                        },
                        'status': 'new'
                    }
                },
                {
                    'node': {
                        'comment': 'Jupiter',
                        'details': '{"data": "restored", "more": true}',
                        'id': 'SXNzdWU6Mw==',
                        'kindKey': 'pride-moran:john',
                        'lastCheck': '2018-09-03 13:09:21.022164+00:00',
                        'remoteIssueId': 6346,
                        'repository': {
                            'id': 'UmVwb3NpdG9yeTozOA==',
                            'name': 'bomer',
                            'owner': 'john',
                            'remoteId': 987,
                            'url': 'https://home.com/url'
                        },
                        'status': 'new'
                    }
                },
                {
                    'node': {
                        'comment': 'Herse',
                        'details': '{"data": "restored", "power": true}',
                        'id': 'SXNzdWU6NA==',
                        'kindKey': 'denis:roman',
                        'lastCheck': '2018-09-03 13:09:21.022164+00:00',
                        'remoteIssueId': 9346,
                        'repository': {
                            'id': 'UmVwb3NpdG9yeTozOQ==',
                            'name': 'jackson',
                            'owner': 'john',
                            'remoteId': 246,
                            'url': 'https://home.com/url'
                        },
                        'status': 'new'
                    }
                },
                {
                    'node': {
                        'comment': 'Pluto',
                        'details': '{"data": "restored", "now!": true}',
                        'id': 'SXNzdWU6NQ==',
                        'kindKey': 'dennis:moran',
                        'lastCheck': '2018-09-03 13:09:21.022164+00:00',
                        'remoteIssueId': 65,
                        'repository': {
                            'id': 'UmVwb3NpdG9yeTo0MA==',
                            'name': 'musher',
                            'owner': 'john',
                            'remoteId': 2334,
                            'url': 'https://home.com/url'
                        },
                        'status': 'new'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'NQ==',
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': 'MQ=='
            },
            'totalCount': 5
        }
    }
}

snapshots['test_last 1'] = {
    'data': {
        'allIssues': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 7,
                    'line': 3
                }
            ],
            'message': 'Pagination "last" works only in combination with "before" argument.',
            'path': [
                'allIssues'
            ]
        }
    ]
}
