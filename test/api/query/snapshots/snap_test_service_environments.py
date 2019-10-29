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
                        'allEnvironments': {
                            'edges': [
                                {
                                    'node': {
                                        'dashboardUrl': 'https://dashboardurlD',
                                        'healthCheckUrl': 'https://healthcheckurlD',
                                        'id': 'RW52aXJvbm1lbnQ6NA==',
                                        'name': 'staging3',
                                        'serviceUrls': [
                                            'https://serviceurlD1',
                                            'https://serviceurlD2'
                                        ]
                                    }
                                },
                                {
                                    'node': {
                                        'dashboardUrl': 'https://dashboardurlC',
                                        'healthCheckUrl': 'https://healthcheckurlC',
                                        'id': 'RW52aXJvbm1lbnQ6Mw==',
                                        'name': 'staging2',
                                        'serviceUrls': [
                                            'https://serviceurlC1',
                                            'https://serviceurlC2'
                                        ]
                                    }
                                },
                                {
                                    'node': {
                                        'dashboardUrl': 'https://dashboardurlB',
                                        'healthCheckUrl': 'https://healthcheckurlB',
                                        'id': 'RW52aXJvbm1lbnQ6Mg==',
                                        'name': 'staging',
                                        'serviceUrls': [
                                            'https://serviceurlB1',
                                            'https://serviceurlB2'
                                        ]
                                    }
                                },
                                {
                                    'node': {
                                        'dashboardUrl': 'https://dashboardurlA',
                                        'healthCheckUrl': 'https://healthcheckurlA',
                                        'id': 'RW52aXJvbm1lbnQ6MQ==',
                                        'name': 'production',
                                        'serviceUrls': [
                                            'https://serviceurlA1',
                                            'https://serviceurlA2'
                                        ]
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'NA==',
                                'hasNextPage': False,
                                'hasPreviousPage': False,
                                'startCursor': 'MQ=='
                            },
                            'totalCount': 4
                        }
                    }
                }
            ],
            'totalCount': 1
        }
    }
}

snapshots['test_first 1'] = {
    'data': {
        'allServices': {
            'edges': [
                {
                    'node': {
                        'allEnvironments': {
                            'edges': [
                                {
                                    'node': {
                                        'dashboardUrl': 'https://dashboardurlD',
                                        'healthCheckUrl': 'https://healthcheckurlD',
                                        'id': 'RW52aXJvbm1lbnQ6NA==',
                                        'name': 'staging3',
                                        'serviceUrls': [
                                            'https://serviceurlD1',
                                            'https://serviceurlD2'
                                        ]
                                    }
                                },
                                {
                                    'node': {
                                        'dashboardUrl': 'https://dashboardurlC',
                                        'healthCheckUrl': 'https://healthcheckurlC',
                                        'id': 'RW52aXJvbm1lbnQ6Mw==',
                                        'name': 'staging2',
                                        'serviceUrls': [
                                            'https://serviceurlC1',
                                            'https://serviceurlC2'
                                        ]
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'Mg==',
                                'hasNextPage': True,
                                'hasPreviousPage': False,
                                'startCursor': 'MQ=='
                            },
                            'totalCount': 4
                        }
                    }
                }
            ],
            'totalCount': 1
        }
    }
}

snapshots['test_last 1'] = {
    'data': {
        'allServices': {
            'edges': [
                {
                    'node': {
                        'allEnvironments': {
                            'edges': [
                                {
                                    'node': {
                                        'dashboardUrl': 'https://dashboardurlD',
                                        'healthCheckUrl': 'https://healthcheckurlD',
                                        'id': 'RW52aXJvbm1lbnQ6NA==',
                                        'name': 'staging3',
                                        'serviceUrls': [
                                            'https://serviceurlD1',
                                            'https://serviceurlD2'
                                        ]
                                    }
                                }
                            ],
                            'pageInfo': {
                                'endCursor': 'MQ==',
                                'hasNextPage': True,
                                'hasPreviousPage': False,
                                'startCursor': 'MQ=='
                            },
                            'totalCount': 4
                        }
                    }
                }
            ],
            'totalCount': 1
        }
    }
}
