# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_empty 1'] = {
    'data': {
        'allDependencyUsages': {
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
                },
                {
                    'node': {
                        'forProduction': 'false',
                        'id': 'RGVwZW5kZW5jeVVzYWdlOjI=',
                        'majorVersion': 3,
                        'minorVersion': 4,
                        'patchVersion': 6,
                        'version': '3.4.6'
                    }
                },
                {
                    'node': {
                        'forProduction': 'false',
                        'id': 'RGVwZW5kZW5jeVVzYWdlOjM=',
                        'majorVersion': 3,
                        'minorVersion': 5,
                        'patchVersion': 1,
                        'version': '3.5.1'
                    }
                },
                {
                    'node': {
                        'forProduction': 'false',
                        'id': 'RGVwZW5kZW5jeVVzYWdlOjQ=',
                        'majorVersion': 2,
                        'minorVersion': 5,
                        'patchVersion': 1,
                        'version': '2.5.1'
                    }
                },
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
                },
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
                },
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
                'endCursor': 'NA==',
                'hasNextPage': True,
                'hasPreviousPage': True,
                'startCursor': 'Mw=='
            },
            'totalCount': 5
        }
    }
}

snapshots['test_last 1'] = {
    'data': {
        'allDependencyUsages': None
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
                'allDependencyUsages'
            ]
        }
    ]
}

snapshots['test_last_before 1'] = {
    'data': {
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
                'hasNextPage': True,
                'hasPreviousPage': False,
                'startCursor': 'MQ=='
            },
            'totalCount': 5
        }
    }
}

snapshots['test_with_dependency 1'] = {
    'data': {
        'allDependencyUsages': {
            'edges': [
                {
                    'node': {
                        'dependency': {
                            'id': 'RGVwZW5kZW5jeTozNA==',
                            'name': 'graphql',
                            'type': 'Python Library'
                        },
                        'forProduction': 'true',
                        'id': 'RGVwZW5kZW5jeVVzYWdlOjE=',
                        'majorVersion': 3,
                        'minorVersion': 4,
                        'patchVersion': 6,
                        'version': '3.4.6'
                    }
                },
                {
                    'node': {
                        'dependency': {
                            'id': 'RGVwZW5kZW5jeTozMA==',
                            'name': 'html',
                            'type': 'Language'
                        },
                        'forProduction': 'false',
                        'id': 'RGVwZW5kZW5jeVVzYWdlOjI=',
                        'majorVersion': 3,
                        'minorVersion': 4,
                        'patchVersion': 6,
                        'version': '3.4.6'
                    }
                },
                {
                    'node': {
                        'dependency': {
                            'id': 'RGVwZW5kZW5jeToyOQ==',
                            'name': 'vue',
                            'type': 'Language'
                        },
                        'forProduction': 'false',
                        'id': 'RGVwZW5kZW5jeVVzYWdlOjM=',
                        'majorVersion': 3,
                        'minorVersion': 5,
                        'patchVersion': 1,
                        'version': '3.5.1'
                    }
                },
                {
                    'node': {
                        'dependency': {
                            'id': 'RGVwZW5kZW5jeToyOA==',
                            'name': 'arrow',
                            'type': 'Python Library'
                        },
                        'forProduction': 'false',
                        'id': 'RGVwZW5kZW5jeVVzYWdlOjQ=',
                        'majorVersion': 2,
                        'minorVersion': 5,
                        'patchVersion': 1,
                        'version': '2.5.1'
                    }
                },
                {
                    'node': {
                        'dependency': {
                            'id': 'RGVwZW5kZW5jeTozMQ==',
                            'name': 'graphql',
                            'type': 'Javascript Library'
                        },
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
                'endCursor': 'NQ==',
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': 'MQ=='
            },
            'totalCount': 5
        }
    }
}

snapshots['test_with_repository 1'] = {
    'data': {
        'allDependencyUsages': {
            'edges': [
                {
                    'node': {
                        'forProduction': 'true',
                        'id': 'RGVwZW5kZW5jeVVzYWdlOjE=',
                        'majorVersion': 3,
                        'minorVersion': 4,
                        'patchVersion': 6,
                        'repository': {
                            'id': 'UmVwb3NpdG9yeToxMzM5',
                            'name': 'lowe',
                            'owner': 'dadivgross',
                            'remoteId': 2434,
                            'url': 'https://gitlab.com/davidgross/lowe'
                        },
                        'version': '3.4.6'
                    }
                },
                {
                    'node': {
                        'forProduction': 'false',
                        'id': 'RGVwZW5kZW5jeVVzYWdlOjI=',
                        'majorVersion': 3,
                        'minorVersion': 4,
                        'patchVersion': 6,
                        'repository': {
                            'id': 'UmVwb3NpdG9yeToxNDMyNA==',
                            'name': 'john',
                            'owner': 'malkovic',
                            'remoteId': 434,
                            'url': 'https://gitlab.com/malkovic/john'
                        },
                        'version': '3.4.6'
                    }
                },
                {
                    'node': {
                        'forProduction': 'false',
                        'id': 'RGVwZW5kZW5jeVVzYWdlOjM=',
                        'majorVersion': 3,
                        'minorVersion': 5,
                        'patchVersion': 1,
                        'repository': {
                            'id': 'UmVwb3NpdG9yeToxMw==',
                            'name': 'xscott',
                            'owner': 'brownkendra',
                            'remoteId': 9949,
                            'url': 'https://gitlab.com/brownkendra/xscott'
                        },
                        'version': '3.5.1'
                    }
                },
                {
                    'node': {
                        'forProduction': 'false',
                        'id': 'RGVwZW5kZW5jeVVzYWdlOjQ=',
                        'majorVersion': 2,
                        'minorVersion': 5,
                        'patchVersion': 1,
                        'repository': {
                            'id': 'UmVwb3NpdG9yeToxOA==',
                            'name': 'cole',
                            'owner': 'ismith',
                            'remoteId': 3599,
                            'url': 'https://gitlab.com/ismith/cole'
                        },
                        'version': '2.5.1'
                    }
                },
                {
                    'node': {
                        'forProduction': 'true',
                        'id': 'RGVwZW5kZW5jeVVzYWdlOjU=',
                        'majorVersion': 1,
                        'minorVersion': 2,
                        'patchVersion': 2,
                        'repository': {
                            'id': 'UmVwb3NpdG9yeTozMzI0OA==',
                            'name': 'rachel39',
                            'owner': 'martinez',
                            'remoteId': 39823,
                            'url': 'https://gitlab.com/martinez/rachel39'
                        },
                        'version': '1.2.2'
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
