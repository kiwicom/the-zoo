# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_empty 1'] = {
    'data': {
        'allServices': {
            'edges': [
            ],
            'totalCount': 0
        }
    }
}

snapshots['test_all 1'] = {
    'data': {
        'allServices': {
            'edges': [
                {
                    'node': {
                        'docsUrl': 'https://docsurl',
                        'id': 'U2VydmljZTox',
                        'impact': 'profit',
                        'name': 'martinez',
                        'owner': 'michaelbennett',
                        'pagerdutyUrl': 'https://pagerduty',
                        'slackChannel': 'https://slackchannel',
                        'status': 'fixed'
                    }
                },
                {
                    'node': {
                        'docsUrl': 'https://docsurl',
                        'id': 'U2VydmljZToy',
                        'impact': 'profit',
                        'name': 'alex',
                        'owner': 'amstrong',
                        'pagerdutyUrl': 'https://pagerduty',
                        'slackChannel': 'https://slackchannel',
                        'status': 'fixed'
                    }
                },
                {
                    'node': {
                        'docsUrl': 'https://docsurl',
                        'id': 'U2VydmljZToz',
                        'impact': 'profit',
                        'name': 'artinez',
                        'owner': 'bennett',
                        'pagerdutyUrl': 'https://pagerduty',
                        'slackChannel': 'https://slackchannel',
                        'status': 'fixed'
                    }
                },
                {
                    'node': {
                        'docsUrl': 'https://docsurl',
                        'id': 'U2VydmljZTo0',
                        'impact': 'profit',
                        'name': 'john',
                        'owner': 'benneto',
                        'pagerdutyUrl': 'https://pagerduty',
                        'slackChannel': 'https://slackchannel',
                        'status': 'fixed'
                    }
                },
                {
                    'node': {
                        'docsUrl': 'https://docsurl',
                        'id': 'U2VydmljZToxMg==',
                        'impact': 'profit',
                        'name': 'simmons-mitchell',
                        'owner': 'dedward',
                        'pagerdutyUrl': 'https://pagerduty',
                        'slackChannel': 'https://slackchannel',
                        'status': 'fixed'
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
        'allServices': {
            'edges': [
                {
                    'node': {
                        'docsUrl': 'https://docsurl',
                        'id': 'U2VydmljZTox',
                        'impact': 'profit',
                        'name': 'martinez',
                        'owner': 'michaelbennett',
                        'pagerdutyUrl': 'https://pagerduty',
                        'repository': {
                            'name': 'thiwer',
                            'owner': 'jasckson',
                            'remoteId': 239,
                            'url': 'https://gitlab.com/thiwer/thiwer'
                        },
                        'slackChannel': 'https://slackchannel',
                        'status': 'fixed'
                    }
                },
                {
                    'node': {
                        'docsUrl': 'https://docsurl',
                        'id': 'U2VydmljZToy',
                        'impact': 'profit',
                        'name': 'alex',
                        'owner': 'amstrong',
                        'pagerdutyUrl': 'https://pagerduty',
                        'repository': {
                            'name': 'farel',
                            'owner': 'colisn',
                            'remoteId': 99,
                            'url': 'https://gitlab.com/farel/colins'
                        },
                        'slackChannel': 'https://slackchannel',
                        'status': 'fixed'
                    }
                },
                {
                    'node': {
                        'docsUrl': 'https://docsurl',
                        'id': 'U2VydmljZToz',
                        'impact': 'profit',
                        'name': 'artinez',
                        'owner': 'bennett',
                        'pagerdutyUrl': 'https://pagerduty',
                        'repository': {
                            'name': 'Amstrong',
                            'owner': 'Daniel',
                            'remoteId': 9234,
                            'url': 'https://gitlab.com/daniel/amstrong'
                        },
                        'slackChannel': 'https://slackchannel',
                        'status': 'fixed'
                    }
                },
                {
                    'node': {
                        'docsUrl': 'https://docsurl',
                        'id': 'U2VydmljZTo0',
                        'impact': 'profit',
                        'name': 'john',
                        'owner': 'benneto',
                        'pagerdutyUrl': 'https://pagerduty',
                        'repository': {
                            'name': 'blanc',
                            'owner': 'josh',
                            'remoteId': 349,
                            'url': 'https://gitlab.com/josh/blanc'
                        },
                        'slackChannel': 'https://slackchannel',
                        'status': 'fixed'
                    }
                },
                {
                    'node': {
                        'docsUrl': 'https://docsurl',
                        'id': 'U2VydmljZToxMg==',
                        'impact': 'profit',
                        'name': 'simmons-mitchell',
                        'owner': 'dedward',
                        'pagerdutyUrl': 'https://pagerduty',
                        'repository': {
                            'name': 'leblanc',
                            'owner': 'imosley',
                            'remoteId': 990,
                            'url': 'https://gitlab.com/schultzcarolyn/leblanc'
                        },
                        'slackChannel': 'https://slackchannel',
                        'status': 'fixed'
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
        'allServices': {
            'edges': [
                {
                    'node': {
                        'docsUrl': 'https://docsurl',
                        'id': 'U2VydmljZTox',
                        'impact': 'profit',
                        'owner': 'michaelbennett',
                        'pagerdutyUrl': 'https://pagerduty',
                        'slackChannel': 'https://slackchannel',
                        'status': 'fixed'
                    }
                },
                {
                    'node': {
                        'docsUrl': 'https://docsurl',
                        'id': 'U2VydmljZToy',
                        'impact': 'profit',
                        'owner': 'amstrong',
                        'pagerdutyUrl': 'https://pagerduty',
                        'slackChannel': 'https://slackchannel',
                        'status': 'fixed'
                    }
                },
                {
                    'node': {
                        'docsUrl': 'https://docsurl',
                        'id': 'U2VydmljZToz',
                        'impact': 'profit',
                        'owner': 'bennett',
                        'pagerdutyUrl': 'https://pagerduty',
                        'slackChannel': 'https://slackchannel',
                        'status': 'fixed'
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
        'allServices': {
            'edges': [
                {
                    'node': {
                        'docsUrl': 'https://docsurl',
                        'id': 'U2VydmljZToy',
                        'impact': 'profit',
                        'owner': 'amstrong',
                        'pagerdutyUrl': 'https://pagerduty',
                        'slackChannel': 'https://slackchannel',
                        'status': 'fixed'
                    }
                },
                {
                    'node': {
                        'docsUrl': 'https://docsurl',
                        'id': 'U2VydmljZToz',
                        'impact': 'profit',
                        'owner': 'bennett',
                        'pagerdutyUrl': 'https://pagerduty',
                        'slackChannel': 'https://slackchannel',
                        'status': 'fixed'
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
        'allServices': {
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

snapshots['test_last 1'] = {
    'data': {
        'allServices': None
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
                'allServices'
            ]
        }
    ]
}

snapshots['test_with_environment 1'] = {
    'data': {
        'allServices': {
            'edges': [
                {
                    'node': {
                        'allEnvironments': {
                            'edges': [
                                {
                                    'node': {
                                        'dashboardUrl': 'https://dashboardurl',
                                        'healthCheckUrl': 'https://healthcheckurl',
                                        'name': 'staging',
                                        'serviceUrls': [
                                            'https://serviceurl1',
                                            'https://serviceurl2'
                                        ]
                                    }
                                },
                                {
                                    'node': {
                                        'dashboardUrl': 'https://dashboardurl',
                                        'healthCheckUrl': 'https://healthcheckurl',
                                        'name': 'production',
                                        'serviceUrls': [
                                            'https://serviceurl1',
                                            'https://serviceurl2'
                                        ]
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
                        },
                        'docsUrl': 'https://docsurl',
                        'id': 'U2VydmljZTox',
                        'impact': 'profit',
                        'name': 'martinez',
                        'owner': 'michaelbennett',
                        'pagerdutyUrl': 'https://pagerduty',
                        'slackChannel': 'https://slackchannel',
                        'status': 'fixed'
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
