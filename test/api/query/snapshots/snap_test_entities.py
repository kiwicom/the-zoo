# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_all 1'] = {
    'data': {
        'allEntities': {
            'edges': [
                {
                    'node': {
                        'description': 'This is my fancy component',
                        'id': 'RW50aXR5OjE=',
                        'kind': None,
                        'label': 'Base',
                        'name': 'base',
                        'owner': 'platform',
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy component 2',
                        'id': 'RW50aXR5OjI=',
                        'kind': None,
                        'label': 'Base 2',
                        'name': 'base_2',
                        'owner': 'platformm2',
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy component 3',
                        'id': 'RW50aXR5OjMy',
                        'kind': None,
                        'label': 'Base 3',
                        'name': 'base_3',
                        'owner': 'platformm3',
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy service',
                        'id': 'RW50aXR5OjEyNDU=',
                        'kind': None,
                        'label': 'Service',
                        'name': 'service',
                        'owner': 'platform',
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy library',
                        'id': 'RW50aXR5OjE1NTQ1',
                        'kind': None,
                        'label': 'Library',
                        'name': 'library',
                        'owner': 'platform',
                        'type': None
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

snapshots['test_empty 1'] = {
    'data': {
        'allEntities': {
            'edges': [
            ],
            'totalCount': 0
        }
    }
}

snapshots['test_first 1'] = {
    'data': {
        'allEntities': {
            'edges': [
                {
                    'node': {
                        'description': 'This is my fancy component',
                        'id': 'RW50aXR5OjE=',
                        'kind': None,
                        'label': 'Base',
                        'name': 'base',
                        'owner': 'platform',
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy component 2',
                        'id': 'RW50aXR5OjI=',
                        'kind': None,
                        'label': 'Base 2',
                        'name': 'base_2',
                        'owner': 'platformm2',
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy component 3',
                        'id': 'RW50aXR5OjMy',
                        'kind': None,
                        'label': 'Base 3',
                        'name': 'base_3',
                        'owner': 'platformm3',
                        'type': None
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
        'allEntities': {
            'edges': [
                {
                    'node': {
                        'description': 'This is my fancy component 2',
                        'id': 'RW50aXR5OjI=',
                        'kind': None,
                        'label': 'Base 2',
                        'name': 'base_2',
                        'owner': 'platformm2',
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy component 3',
                        'id': 'RW50aXR5OjMy',
                        'kind': None,
                        'label': 'Base 3',
                        'name': 'base_3',
                        'owner': 'platformm3',
                        'type': None
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

snapshots['test_last 1'] = {
    'data': {
        'allEntities': None
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
                'allEntities'
            ]
        }
    ]
}

snapshots['test_last_before 1'] = {
    'data': {
        'allEntities': {
            'edges': [
            ],
            'pageInfo': {
                'endCursor': None,
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': None
            },
            'totalCount': 5
        }
    }
}

snapshots['test_with_group 1'] = {
    'data': {
        'allEntities': {
            'edges': [
                {
                    'node': {
                        'description': 'This is my fancy component',
                        'group': {
                            'maintainers': [
                            ],
                            'productOwner': 'wallacebrian',
                            'projectOwner': 'ktorres'
                        },
                        'id': 'RW50aXR5OjE=',
                        'kind': None,
                        'label': 'Base',
                        'name': 'base',
                        'owner': 'platform',
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy component 2',
                        'group': {
                            'maintainers': [
                            ],
                            'productOwner': 'twatson',
                            'projectOwner': 'cartermatthew'
                        },
                        'id': 'RW50aXR5OjI=',
                        'kind': None,
                        'label': 'Base 2',
                        'name': 'base_2',
                        'owner': 'platformm2',
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy component 3',
                        'group': {
                            'maintainers': [
                            ],
                            'productOwner': 'jason33',
                            'projectOwner': 'gomezjonathan'
                        },
                        'id': 'RW50aXR5OjMy',
                        'kind': None,
                        'label': 'Base 3',
                        'name': 'base_3',
                        'owner': 'platformm3',
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy service',
                        'group': {
                            'maintainers': [
                            ],
                            'productOwner': 'jeffrey52',
                            'projectOwner': 'kari29'
                        },
                        'id': 'RW50aXR5OjEyNDU=',
                        'kind': None,
                        'label': 'Service',
                        'name': 'service',
                        'owner': 'platform',
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy library',
                        'group': {
                            'maintainers': [
                            ],
                            'productOwner': 'vmelendez',
                            'projectOwner': 'wrivera'
                        },
                        'id': 'RW50aXR5OjE1NTQ1',
                        'kind': None,
                        'label': 'Library',
                        'name': 'library',
                        'owner': 'platform',
                        'type': None
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

snapshots['test_with_library 1'] = {
    'data': {
        'allEntities': {
            'edges': [
                {
                    'node': {
                        'description': 'This is my fancy component',
                        'id': 'RW50aXR5OjE=',
                        'kind': None,
                        'label': 'Base',
                        'library': None,
                        'name': 'base',
                        'owner': 'platform',
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy component 2',
                        'id': 'RW50aXR5OjI=',
                        'kind': None,
                        'label': 'Base 2',
                        'library': None,
                        'name': 'base_2',
                        'owner': 'platformm2',
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy component 3',
                        'id': 'RW50aXR5OjMy',
                        'kind': None,
                        'label': 'Base 3',
                        'library': None,
                        'name': 'base_3',
                        'owner': 'platformm3',
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy service',
                        'id': 'RW50aXR5OjEyNDU=',
                        'kind': None,
                        'label': 'Service',
                        'library': None,
                        'name': 'service',
                        'owner': 'platform',
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy library',
                        'id': 'RW50aXR5OjE1NTQ1',
                        'kind': None,
                        'label': 'Library',
                        'library': {
                            'docsUrl': None,
                            'impact': 'employees',
                            'libraryUrl': None,
                            'lifecycle': 'beta',
                            'name': 'clark',
                            'owner': 'carolyn61',
                            'slackChannel': 'lewis',
                            'sonarqubeProject': 'lin'
                        },
                        'name': 'library',
                        'owner': 'platform',
                        'type': None
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

snapshots['test_with_links 1'] = {
    'data': {
        'allEntities': {
            'edges': [
                {
                    'node': {
                        'allLinks': {
                            'edges': [
                                {
                                    'node': {
                                        'icon': 'poop',
                                        'name': 'Datadog',
                                        'url': 'https://dashboard.datadog.com'
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
                        'description': 'This is my fancy component',
                        'id': 'RW50aXR5OjE=',
                        'kind': None,
                        'label': 'Base',
                        'name': 'base',
                        'owner': 'platform',
                        'type': None
                    }
                },
                {
                    'node': {
                        'allLinks': {
                            'edges': [
                                {
                                    'node': {
                                        'icon': None,
                                        'name': 'Sentry',
                                        'url': 'https://sentry.skypicker.com'
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
                        'description': 'This is my fancy component 2',
                        'id': 'RW50aXR5OjI=',
                        'kind': None,
                        'label': 'Base 2',
                        'name': 'base_2',
                        'owner': 'platformm2',
                        'type': None
                    }
                },
                {
                    'node': {
                        'allLinks': {
                            'edges': [
                            ],
                            'pageInfo': {
                                'endCursor': None,
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': None
                            },
                            'totalCount': 0
                        },
                        'description': 'This is my fancy component 3',
                        'id': 'RW50aXR5OjMy',
                        'kind': None,
                        'label': 'Base 3',
                        'name': 'base_3',
                        'owner': 'platformm3',
                        'type': None
                    }
                },
                {
                    'node': {
                        'allLinks': {
                            'edges': [
                            ],
                            'pageInfo': {
                                'endCursor': None,
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': None
                            },
                            'totalCount': 0
                        },
                        'description': 'This is my fancy service',
                        'id': 'RW50aXR5OjEyNDU=',
                        'kind': None,
                        'label': 'Service',
                        'name': 'service',
                        'owner': 'platform',
                        'type': None
                    }
                },
                {
                    'node': {
                        'allLinks': {
                            'edges': [
                            ],
                            'pageInfo': {
                                'endCursor': None,
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': None
                            },
                            'totalCount': 0
                        },
                        'description': 'This is my fancy library',
                        'id': 'RW50aXR5OjE1NTQ1',
                        'kind': None,
                        'label': 'Library',
                        'name': 'library',
                        'owner': 'platform',
                        'type': None
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

snapshots['test_with_service 1'] = {
    'data': {
        'allEntities': {
            'edges': [
                {
                    'node': {
                        'description': 'This is my fancy component',
                        'id': 'RW50aXR5OjE=',
                        'kind': None,
                        'label': 'Base',
                        'name': 'base',
                        'owner': 'platform',
                        'service': None,
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy component 2',
                        'id': 'RW50aXR5OjI=',
                        'kind': None,
                        'label': 'Base 2',
                        'name': 'base_2',
                        'owner': 'platformm2',
                        'service': None,
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy component 3',
                        'id': 'RW50aXR5OjMy',
                        'kind': None,
                        'label': 'Base 3',
                        'name': 'base_3',
                        'owner': 'platformm3',
                        'service': None,
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy service',
                        'id': 'RW50aXR5OjEyNDU=',
                        'kind': None,
                        'label': 'Service',
                        'name': 'service',
                        'owner': 'platform',
                        'service': {
                            'docsUrl': 'https://docs.com',
                            'id': 'U2VydmljZToz',
                            'impact': 'employees',
                            'lifecycle': 'production',
                            'owner': 'platform',
                            'pagerdutyService': None,
                            'slackChannel': '#platform-software'
                        },
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy library',
                        'id': 'RW50aXR5OjE1NTQ1',
                        'kind': None,
                        'label': 'Library',
                        'name': 'library',
                        'owner': 'platform',
                        'service': None,
                        'type': None
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

snapshots['test_with_source 1'] = {
    'data': {
        'allEntities': {
            'edges': [
                {
                    'node': {
                        'description': 'This is my fancy component',
                        'id': 'RW50aXR5OjE=',
                        'kind': None,
                        'label': 'Base',
                        'name': 'base',
                        'owner': 'platform',
                        'source': None,
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy component 2',
                        'id': 'RW50aXR5OjI=',
                        'kind': None,
                        'label': 'Base 2',
                        'name': 'base_2',
                        'owner': 'platformm2',
                        'source': None,
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy component 3',
                        'id': 'RW50aXR5OjMy',
                        'kind': None,
                        'label': 'Base 3',
                        'name': 'base_3',
                        'owner': 'platformm3',
                        'source': None,
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy service',
                        'id': 'RW50aXR5OjEyNDU=',
                        'kind': None,
                        'label': 'Service',
                        'name': 'service',
                        'owner': 'platform',
                        'source': None,
                        'type': None
                    }
                },
                {
                    'node': {
                        'description': 'This is my fancy library',
                        'id': 'RW50aXR5OjE1NTQ1',
                        'kind': None,
                        'label': 'Library',
                        'name': 'library',
                        'owner': 'platform',
                        'source': None,
                        'type': None
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
