# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_empty 1'] = {
    'data': {
        'allDependencies': {
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
        'allDependencies': {
            'edges': [
                {
                    'node': {
                        'id': 'RGVwZW5kZW5jeTozNA==',
                        'name': 'graphql',
                        'type': 'Python Library'
                    }
                },
                {
                    'node': {
                        'id': 'RGVwZW5kZW5jeTozMA==',
                        'name': 'html',
                        'type': 'Language'
                    }
                },
                {
                    'node': {
                        'id': 'RGVwZW5kZW5jeToyOQ==',
                        'name': 'vue',
                        'type': 'Language'
                    }
                },
                {
                    'node': {
                        'id': 'RGVwZW5kZW5jeToyOA==',
                        'name': 'arrow',
                        'type': 'Python Library'
                    }
                },
                {
                    'node': {
                        'id': 'RGVwZW5kZW5jeTozMQ==',
                        'name': 'graphql',
                        'type': 'Javascript Library'
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
        'allDependencies': {
            'edges': [
                {
                    'node': {
                        'id': 'RGVwZW5kZW5jeTozNA==',
                        'name': 'graphql',
                        'type': 'Python Library'
                    }
                },
                {
                    'node': {
                        'id': 'RGVwZW5kZW5jeTozMA==',
                        'name': 'html',
                        'type': 'Language'
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
        'allDependencies': {
            'edges': [
                {
                    'node': {
                        'id': 'RGVwZW5kZW5jeToyOQ==',
                        'name': 'vue',
                        'type': 'Language'
                    }
                },
                {
                    'node': {
                        'id': 'RGVwZW5kZW5jeToyOA==',
                        'name': 'arrow',
                        'type': 'Python Library'
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
        'allDependencies': None
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
                'allDependencies'
            ]
        }
    ]
}

snapshots['test_last_before 1'] = {
    'data': {
        'allDependencies': {
            'edges': [
                {
                    'node': {
                        'id': 'RGVwZW5kZW5jeTozNA==',
                        'name': 'graphql',
                        'type': 'Python Library'
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

snapshots['test_with_dependency_usage 1'] = {
    'data': {
        'allDependencies': {
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
                            ]
                        },
                        'id': 'RGVwZW5kZW5jeTozNA==',
                        'name': 'graphql',
                        'type': 'Python Library'
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
                            ]
                        },
                        'id': 'RGVwZW5kZW5jeTozMA==',
                        'name': 'html',
                        'type': 'Language'
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
                            ]
                        },
                        'id': 'RGVwZW5kZW5jeToyOQ==',
                        'name': 'vue',
                        'type': 'Language'
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
                            ]
                        },
                        'id': 'RGVwZW5kZW5jeToyOA==',
                        'name': 'arrow',
                        'type': 'Python Library'
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
                            ]
                        },
                        'id': 'RGVwZW5kZW5jeTozMQ==',
                        'name': 'graphql',
                        'type': 'Javascript Library'
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

snapshots['test_filter_by_name 1'] = {
    'data': {
        'allDependencies': {
            'edges': [
                {
                    'node': {
                        'id': 'RGVwZW5kZW5jeTozNA==',
                        'name': 'graphql',
                        'type': 'Python Library'
                    }
                },
                {
                    'node': {
                        'id': 'RGVwZW5kZW5jeTozMQ==',
                        'name': 'graphql',
                        'type': 'Javascript Library'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'Mg==',
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': 'MQ=='
            },
            'totalCount': 2
        }
    }
}

snapshots['test_filter_by_type 1'] = {
    'data': {
        'allDependencies': {
            'edges': [
                {
                    'node': {
                        'id': 'RGVwZW5kZW5jeTozNA==',
                        'name': 'graphql',
                        'type': 'Python Library'
                    }
                },
                {
                    'node': {
                        'id': 'RGVwZW5kZW5jeToyOA==',
                        'name': 'arrow',
                        'type': 'Python Library'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'Mg==',
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': 'MQ=='
            },
            'totalCount': 2
        }
    }
}

snapshots['test_filter_by_type_and_name 1'] = {
    'data': {
        'allDependencies': {
            'edges': [
                {
                    'node': {
                        'id': 'RGVwZW5kZW5jeTozNA==',
                        'name': 'graphql',
                        'type': 'Python Library'
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
        }
    }
}
