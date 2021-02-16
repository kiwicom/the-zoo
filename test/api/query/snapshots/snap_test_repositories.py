# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_all 1'] = {
    'data': {
        'repositories': {
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
                'endCursor': 'YXJyYXljb25uZWN0aW9uOjQ=',
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': 'YXJyYXljb25uZWN0aW9uOjA='
            }
        }
    }
}

snapshots['test_empty 1'] = {
    'data': {
        'repositories': {
            'edges': [
            ],
            'pageInfo': {
                'endCursor': None,
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': None
            }
        }
    }
}

snapshots['test_first 1'] = {
    'data': {
        'repositories': {
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
                'endCursor': 'YXJyYXljb25uZWN0aW9uOjI=',
                'hasNextPage': True,
                'hasPreviousPage': False,
                'startCursor': 'YXJyYXljb25uZWN0aW9uOjA='
            }
        }
    }
}

snapshots['test_first_after 1'] = {
    'data': {
        'repositories': {
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
                }
            ],
            'pageInfo': {
                'endCursor': 'YXJyYXljb25uZWN0aW9uOjE=',
                'hasNextPage': True,
                'hasPreviousPage': False,
                'startCursor': 'YXJyYXljb25uZWN0aW9uOjA='
            }
        }
    }
}

snapshots['test_last 1'] = {
    'data': {
        'repositories': {
            'edges': [
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeToz',
                        'name': 'serr',
                        'owner': 'olivia',
                        'url': 'https://gitlab.com/olivia/serr'
                    }
                },
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeTo0',
                        'name': 'serrano',
                        'owner': 'osbornolivia',
                        'url': 'https://gitlab.com/osbornolivia/serrano'
                    }
                },
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeTo1',
                        'name': 'malboro',
                        'owner': 'tag',
                        'url': 'https://gitlab.com/tag/malboro'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'YXJyYXljb25uZWN0aW9uOjQ=',
                'hasNextPage': False,
                'hasPreviousPage': True,
                'startCursor': 'YXJyYXljb25uZWN0aW9uOjI='
            }
        }
    }
}

snapshots['test_last_before 1'] = {
    'data': {
        'repositories': {
            'edges': [
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeTo1',
                        'name': 'malboro',
                        'owner': 'tag',
                        'url': 'https://gitlab.com/tag/malboro'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'YXJyYXljb25uZWN0aW9uOjQ=',
                'hasNextPage': False,
                'hasPreviousPage': True,
                'startCursor': 'YXJyYXljb25uZWN0aW9uOjQ='
            }
        }
    }
}

snapshots['test_with_dependency_usage 1'] = {
    'data': {
        'repositories': {
            'edges': [
                {
                    'node': {
                        'dependencyUsages': {
                            'edges': [
                                {
                                    'node': {
                                        'forProduction': True,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjE=',
                                        'majorVersion': 3,
                                        'minorVersion': 4,
                                        'patchVersion': 6,
                                        'version': '3.4.6'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': False,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjI=',
                                        'majorVersion': 3,
                                        'minorVersion': 4,
                                        'patchVersion': 6,
                                        'version': '3.4.6'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': False,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjM=',
                                        'majorVersion': 3,
                                        'minorVersion': 5,
                                        'patchVersion': 1,
                                        'version': '3.5.1'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': False,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjQ=',
                                        'majorVersion': 2,
                                        'minorVersion': 5,
                                        'patchVersion': 1,
                                        'version': '2.5.1'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': True,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjU=',
                                        'majorVersion': 1,
                                        'minorVersion': 2,
                                        'patchVersion': 2,
                                        'version': '1.2.2'
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'YXJyYXljb25uZWN0aW9uOjQ=',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'YXJyYXljb25uZWN0aW9uOjA='
                            }
                        },
                        'id': 'UmVwb3NpdG9yeToxMzM5',
                        'name': 'lowe',
                        'owner': 'dadivgross',
                        'url': 'https://gitlab.com/davidgross/lowe'
                    }
                },
                {
                    'node': {
                        'dependencyUsages': {
                            'edges': [
                                {
                                    'node': {
                                        'forProduction': True,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjE=',
                                        'majorVersion': 3,
                                        'minorVersion': 4,
                                        'patchVersion': 6,
                                        'version': '3.4.6'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': False,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjI=',
                                        'majorVersion': 3,
                                        'minorVersion': 4,
                                        'patchVersion': 6,
                                        'version': '3.4.6'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': False,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjM=',
                                        'majorVersion': 3,
                                        'minorVersion': 5,
                                        'patchVersion': 1,
                                        'version': '3.5.1'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': False,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjQ=',
                                        'majorVersion': 2,
                                        'minorVersion': 5,
                                        'patchVersion': 1,
                                        'version': '2.5.1'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': True,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjU=',
                                        'majorVersion': 1,
                                        'minorVersion': 2,
                                        'patchVersion': 2,
                                        'version': '1.2.2'
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'YXJyYXljb25uZWN0aW9uOjQ=',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'YXJyYXljb25uZWN0aW9uOjA='
                            }
                        },
                        'id': 'UmVwb3NpdG9yeToxNDMyNA==',
                        'name': 'john',
                        'owner': 'malkovic',
                        'url': 'https://gitlab.com/malkovic/john'
                    }
                },
                {
                    'node': {
                        'dependencyUsages': {
                            'edges': [
                                {
                                    'node': {
                                        'forProduction': True,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjE=',
                                        'majorVersion': 3,
                                        'minorVersion': 4,
                                        'patchVersion': 6,
                                        'version': '3.4.6'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': False,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjI=',
                                        'majorVersion': 3,
                                        'minorVersion': 4,
                                        'patchVersion': 6,
                                        'version': '3.4.6'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': False,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjM=',
                                        'majorVersion': 3,
                                        'minorVersion': 5,
                                        'patchVersion': 1,
                                        'version': '3.5.1'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': False,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjQ=',
                                        'majorVersion': 2,
                                        'minorVersion': 5,
                                        'patchVersion': 1,
                                        'version': '2.5.1'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': True,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjU=',
                                        'majorVersion': 1,
                                        'minorVersion': 2,
                                        'patchVersion': 2,
                                        'version': '1.2.2'
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'YXJyYXljb25uZWN0aW9uOjQ=',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'YXJyYXljb25uZWN0aW9uOjA='
                            }
                        },
                        'id': 'UmVwb3NpdG9yeToxMw==',
                        'name': 'xscott',
                        'owner': 'brownkendra',
                        'url': 'https://gitlab.com/brownkendra/xscott'
                    }
                },
                {
                    'node': {
                        'dependencyUsages': {
                            'edges': [
                                {
                                    'node': {
                                        'forProduction': True,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjE=',
                                        'majorVersion': 3,
                                        'minorVersion': 4,
                                        'patchVersion': 6,
                                        'version': '3.4.6'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': False,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjI=',
                                        'majorVersion': 3,
                                        'minorVersion': 4,
                                        'patchVersion': 6,
                                        'version': '3.4.6'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': False,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjM=',
                                        'majorVersion': 3,
                                        'minorVersion': 5,
                                        'patchVersion': 1,
                                        'version': '3.5.1'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': False,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjQ=',
                                        'majorVersion': 2,
                                        'minorVersion': 5,
                                        'patchVersion': 1,
                                        'version': '2.5.1'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': True,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjU=',
                                        'majorVersion': 1,
                                        'minorVersion': 2,
                                        'patchVersion': 2,
                                        'version': '1.2.2'
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'YXJyYXljb25uZWN0aW9uOjQ=',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'YXJyYXljb25uZWN0aW9uOjA='
                            }
                        },
                        'id': 'UmVwb3NpdG9yeToxOA==',
                        'name': 'cole',
                        'owner': 'ismith',
                        'url': 'https://gitlab.com/ismith/cole'
                    }
                },
                {
                    'node': {
                        'dependencyUsages': {
                            'edges': [
                                {
                                    'node': {
                                        'forProduction': True,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjE=',
                                        'majorVersion': 3,
                                        'minorVersion': 4,
                                        'patchVersion': 6,
                                        'version': '3.4.6'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': False,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjI=',
                                        'majorVersion': 3,
                                        'minorVersion': 4,
                                        'patchVersion': 6,
                                        'version': '3.4.6'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': False,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjM=',
                                        'majorVersion': 3,
                                        'minorVersion': 5,
                                        'patchVersion': 1,
                                        'version': '3.5.1'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': False,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjQ=',
                                        'majorVersion': 2,
                                        'minorVersion': 5,
                                        'patchVersion': 1,
                                        'version': '2.5.1'
                                    }
                                },
                                {
                                    'node': {
                                        'forProduction': True,
                                        'id': 'RGVwZW5kZW5jeVVzYWdlOjU=',
                                        'majorVersion': 1,
                                        'minorVersion': 2,
                                        'patchVersion': 2,
                                        'version': '1.2.2'
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'YXJyYXljb25uZWN0aW9uOjQ=',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'YXJyYXljb25uZWN0aW9uOjA='
                            }
                        },
                        'id': 'UmVwb3NpdG9yeTozMzI0OA==',
                        'name': 'rachel39',
                        'owner': 'martinez',
                        'url': 'https://gitlab.com/martinez/rachel39'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'YXJyYXljb25uZWN0aW9uOjQ=',
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': 'YXJyYXljb25uZWN0aW9uOjA='
            }
        }
    }
}

snapshots['test_with_issue 1'] = {
    'data': {
        'repositories': {
            'edges': [
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeTozNg==',
                        'issues': {
                            'edges': [
                                {
                                    'node': {
                                        'comment': 'Saturn',
                                        'details': '{"I": true, "data": "restored"}',
                                        'id': 'SXNzdWU6MQ==',
                                        'kindKey': 'moran:alex',
                                        'lastCheck': '2018-09-03T13:09:21.022164+00:00',
                                        'remoteIssueId': 62,
                                        'status': 'NEW'
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'YXJyYXljb25uZWN0aW9uOjA=',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'YXJyYXljb25uZWN0aW9uOjA='
                            }
                        },
                        'name': 'blumed',
                        'owner': 'john',
                        'url': 'https://home.com/url'
                    }
                },
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeTozNw==',
                        'issues': {
                            'edges': [
                                {
                                    'node': {
                                        'comment': 'Juno',
                                        'details': '{"data": "restored", "need": true}',
                                        'id': 'SXNzdWU6Mg==',
                                        'kindKey': 'cook:alice',
                                        'lastCheck': '2018-09-03T13:09:21.022164+00:00',
                                        'remoteIssueId': 636,
                                        'status': 'NEW'
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'YXJyYXljb25uZWN0aW9uOjA=',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'YXJyYXljb25uZWN0aW9uOjA='
                            }
                        },
                        'name': 'fisher',
                        'owner': 'john',
                        'url': 'https://home.com/url'
                    }
                },
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeTozOA==',
                        'issues': {
                            'edges': [
                                {
                                    'node': {
                                        'comment': 'Jupiter',
                                        'details': '{"data": "restored", "more": true}',
                                        'id': 'SXNzdWU6Mw==',
                                        'kindKey': 'pride-moran:john',
                                        'lastCheck': '2018-09-03T13:09:21.022164+00:00',
                                        'remoteIssueId': 6346,
                                        'status': 'NEW'
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'YXJyYXljb25uZWN0aW9uOjA=',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'YXJyYXljb25uZWN0aW9uOjA='
                            }
                        },
                        'name': 'bomer',
                        'owner': 'john',
                        'url': 'https://home.com/url'
                    }
                },
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeTozOQ==',
                        'issues': {
                            'edges': [
                                {
                                    'node': {
                                        'comment': 'Herse',
                                        'details': '{"data": "restored", "power": true}',
                                        'id': 'SXNzdWU6NA==',
                                        'kindKey': 'denis:roman',
                                        'lastCheck': '2018-09-03T13:09:21.022164+00:00',
                                        'remoteIssueId': 9346,
                                        'status': 'NEW'
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'YXJyYXljb25uZWN0aW9uOjA=',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'YXJyYXljb25uZWN0aW9uOjA='
                            }
                        },
                        'name': 'jackson',
                        'owner': 'john',
                        'url': 'https://home.com/url'
                    }
                },
                {
                    'node': {
                        'id': 'UmVwb3NpdG9yeTo0MA==',
                        'issues': {
                            'edges': [
                                {
                                    'node': {
                                        'comment': 'Pluto',
                                        'details': '{"data": "restored", "now!": true}',
                                        'id': 'SXNzdWU6NQ==',
                                        'kindKey': 'dennis:moran',
                                        'lastCheck': '2018-09-03T13:09:21.022164+00:00',
                                        'remoteIssueId': 65,
                                        'status': 'NEW'
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'YXJyYXljb25uZWN0aW9uOjA=',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'YXJyYXljb25uZWN0aW9uOjA='
                            }
                        },
                        'name': 'musher',
                        'owner': 'john',
                        'url': 'https://home.com/url'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'YXJyYXljb25uZWN0aW9uOjQ=',
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': 'YXJyYXljb25uZWN0aW9uOjA='
            }
        }
    }
}

snapshots['test_with_project_details 1'] = {
    'data': {
        'repository': None
    }
}
