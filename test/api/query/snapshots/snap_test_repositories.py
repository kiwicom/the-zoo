# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_empty 1'] = {
    'data': {
        'allRepositories': {
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
        'allRepositories': {
            'edges': [
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeTox',
                        'name': 'marshall-evans',
                        'owner': 'pmiranda',
                        'remoteId': 11,
                        'url': 'https://gitlab.com/pmiranda/marshall-evans'
                    }
                },
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeToy',
                        'name': 'evans',
                        'owner': 'orange',
                        'remoteId': 12,
                        'url': 'https://gitlab.com/orange/evans'
                    }
                },
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeToz',
                        'name': 'serr',
                        'owner': 'olivia',
                        'remoteId': 33,
                        'url': 'https://gitlab.com/olivia/serr'
                    }
                },
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeTo0',
                        'name': 'serrano',
                        'owner': 'osbornolivia',
                        'remoteId': 21,
                        'url': 'https://gitlab.com/osbornolivia/serrano'
                    }
                },
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeTo1',
                        'name': 'malboro',
                        'owner': 'tag',
                        'remoteId': 22,
                        'url': 'https://gitlab.com/tag/malboro'
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
        'allRepositories': {
            'edges': [
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeTox',
                        'name': 'marshall-evans',
                        'owner': 'pmiranda',
                        'url': 'https://gitlab.com/pmiranda/marshall-evans'
                    }
                },
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeToy',
                        'name': 'evans',
                        'owner': 'orange',
                        'url': 'https://gitlab.com/orange/evans'
                    }
                },
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeToz',
                        'name': 'serr',
                        'owner': 'olivia',
                        'url': 'https://gitlab.com/olivia/serr'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'Mw==',
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
        'allRepositories': {
            'edges': [
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeToy',
                        'name': 'evans',
                        'owner': 'orange',
                        'url': 'https://gitlab.com/orange/evans'
                    }
                },
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeToz',
                        'name': 'serr',
                        'owner': 'olivia',
                        'url': 'https://gitlab.com/olivia/serr'
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
        'allRepositories': {
            'edges': [
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeTox',
                        'name': 'marshall-evans',
                        'owner': 'pmiranda',
                        'url': 'https://gitlab.com/pmiranda/marshall-evans'
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

snapshots['test_with_issue 1'] = {
    'data': {
        'allRepositories': {
            'edges': [
                {
                    'node': {
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
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'MQ=='
                            },
                            'totalCount': 1
                        },
                        'id': 'UmVwb3NpdG9yeTozNg==',
                        'name': 'blumed',
                        'owner': 'john',
                        'url': 'https://home.com/url'
                    }
                },
                {
                    'node': {
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
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'MQ==',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'MQ=='
                            },
                            'totalCount': 1
                        },
                        'id': 'UmVwb3NpdG9yeTozNw==',
                        'name': 'fisher',
                        'owner': 'john',
                        'url': 'https://home.com/url'
                    }
                },
                {
                    'node': {
                        'allIssues': {
                            'edges': [
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
                                'endCursor': 'MQ==',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'MQ=='
                            },
                            'totalCount': 1
                        },
                        'id': 'UmVwb3NpdG9yeTozOA==',
                        'name': 'bomer',
                        'owner': 'john',
                        'url': 'https://home.com/url'
                    }
                },
                {
                    'node': {
                        'allIssues': {
                            'edges': [
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
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'MQ==',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'MQ=='
                            },
                            'totalCount': 1
                        },
                        'id': 'UmVwb3NpdG9yeTozOQ==',
                        'name': 'jackson',
                        'owner': 'john',
                        'url': 'https://home.com/url'
                    }
                },
                {
                    'node': {
                        'allIssues': {
                            'edges': [
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
                                'endCursor': 'MQ==',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'MQ=='
                            },
                            'totalCount': 1
                        },
                        'id': 'UmVwb3NpdG9yeTo0MA==',
                        'name': 'musher',
                        'owner': 'john',
                        'url': 'https://home.com/url'
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
        'allRepositories': None
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
                'allRepositories'
            ]
        }
    ]
}

snapshots['test_with_dependency_usage 1'] = {
    'data': {
        'allRepositories': {
            'edges': [
                {
                    'node': {
                        'allDependencyUsages': {
                            'edges': [
                                {
                                    'node': {
                                        'forProduction': 'true',
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjE=',
                                        'majorVersion': 3,
                                        'minorVersion': 4,
                                        'patchVersion': 6,
                                        'version': '3.4.6'
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'MQ==',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'MQ=='
                            },
                            'totalCount': 1
                        },
                        'id': 'UmVwb3NpdG9yeToxMzM5',
                        'name': 'lowe',
                        'owner': 'dadivgross',
                        'url': 'https://gitlab.com/davidgross/lowe'
                    }
                },
                {
                    'node': {
                        'allDependencyUsages': {
                            'edges': [
                                {
                                    'node': {
                                        'forProduction': 'false',
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjI=',
                                        'majorVersion': 3,
                                        'minorVersion': 4,
                                        'patchVersion': 6,
                                        'version': '3.4.6'
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'MQ==',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'MQ=='
                            },
                            'totalCount': 1
                        },
                        'id': 'UmVwb3NpdG9yeToxNDMyNA==',
                        'name': 'john',
                        'owner': 'malkovic',
                        'url': 'https://gitlab.com/malkovic/john'
                    }
                },
                {
                    'node': {
                        'allDependencyUsages': {
                            'edges': [
                                {
                                    'node': {
                                        'forProduction': 'false',
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjM=',
                                        'majorVersion': 3,
                                        'minorVersion': 5,
                                        'patchVersion': 1,
                                        'version': '3.5.1'
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'MQ==',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'MQ=='
                            },
                            'totalCount': 1
                        },
                        'id': 'UmVwb3NpdG9yeToxMw==',
                        'name': 'xscott',
                        'owner': 'brownkendra',
                        'url': 'https://gitlab.com/brownkendra/xscott'
                    }
                },
                {
                    'node': {
                        'allDependencyUsages': {
                            'edges': [
                                {
                                    'node': {
                                        'forProduction': 'false',
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjQ=',
                                        'majorVersion': 2,
                                        'minorVersion': 5,
                                        'patchVersion': 1,
                                        'version': '2.5.1'
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'MQ==',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'MQ=='
                            },
                            'totalCount': 1
                        },
                        'id': 'UmVwb3NpdG9yeToxOA==',
                        'name': 'cole',
                        'owner': 'ismith',
                        'url': 'https://gitlab.com/ismith/cole'
                    }
                },
                {
                    'node': {
                        'allDependencyUsages': {
                            'edges': [
                                {
                                    'node': {
                                        'forProduction': 'true',
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjU=',
                                        'majorVersion': 1,
                                        'minorVersion': 2,
                                        'patchVersion': 2,
                                        'version': '1.2.2'
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'MQ==',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'MQ=='
                            },
                            'totalCount': 1
                        },
                        'id': 'UmVwb3NpdG9yeTozMzI0OA==',
                        'name': 'rachel39',
                        'owner': 'martinez',
                        'url': 'https://gitlab.com/martinez/rachel39'
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
