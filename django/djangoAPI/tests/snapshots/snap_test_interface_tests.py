# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['APITestCase::test_1_reserve_assets 1'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24',
                    'id': 24,
                    'parent': 1,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 23 Name',
                    'role_number': 'SITE-ROLE-NUM-23'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 2'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.25',
                    'id': 25,
                    'parent': 24,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 24 Name',
                    'role_number': 'SITE-ROLE-NUM-24'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 3'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.26',
                    'id': 26,
                    'parent': 24,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 25 Name',
                    'role_number': 'SITE-ROLE-NUM-25'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 4'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.27',
                    'id': 27,
                    'parent': 24,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 26 Name',
                    'role_number': 'SITE-ROLE-NUM-26'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 5'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.27.28',
                    'id': 28,
                    'parent': 27,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 27 Name',
                    'role_number': 'SITE-ROLE-NUM-27'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 6'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.27.28.29',
                    'id': 29,
                    'parent': 28,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 28 Name',
                    'role_number': 'SITE-ROLE-NUM-28'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 7'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.30',
                    'id': 30,
                    'parent': 24,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 29 Name',
                    'role_number': 'SITE-ROLE-NUM-29'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 8'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.31',
                    'id': 31,
                    'parent': 24,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 30 Name',
                    'role_number': 'SITE-ROLE-NUM-30'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 9'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.31.32',
                    'id': 32,
                    'parent': 31,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 31 Name',
                    'role_number': 'SITE-ROLE-NUM-31'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 10'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.31.33',
                    'id': 33,
                    'parent': 31,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 32 Name',
                    'role_number': 'SITE-ROLE-NUM-32'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 11'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.31.34',
                    'id': 34,
                    'parent': 31,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 33 Name',
                    'role_number': 'SITE-ROLE-NUM-33'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 12'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.31.34.35',
                    'id': 35,
                    'parent': 34,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 34 Name',
                    'role_number': 'SITE-ROLE-NUM-34'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 13'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.31.34.36',
                    'id': 36,
                    'parent': 34,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 35 Name',
                    'role_number': 'SITE-ROLE-NUM-35'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 14'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.37',
                    'id': 37,
                    'parent': 24,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 36 Name',
                    'role_number': 'SITE-ROLE-NUM-36'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 15'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.37.38',
                    'id': 38,
                    'parent': 37,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 37 Name',
                    'role_number': 'SITE-ROLE-NUM-37'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 16'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.37.38.39',
                    'id': 39,
                    'parent': 38,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 38 Name',
                    'role_number': 'SITE-ROLE-NUM-38'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 17'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.40',
                    'id': 40,
                    'parent': 24,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 39 Name',
                    'role_number': 'SITE-ROLE-NUM-39'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_1_reserve_assets 18'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Pending',
                    'approved': False,
                    'full_path': '1.24.40.41',
                    'id': 41,
                    'parent': 40,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 40 Name',
                    'role_number': 'SITE-ROLE-NUM-40'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 1'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24',
                    'id': 24,
                    'parent': 1,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 23 Name',
                    'role_number': 'SITE-ROLE-NUM-23'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 2'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.25',
                    'id': 25,
                    'parent': 24,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 24 Name',
                    'role_number': 'SITE-ROLE-NUM-24'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 3'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.26',
                    'id': 26,
                    'parent': 24,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 25 Name',
                    'role_number': 'SITE-ROLE-NUM-25'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 4'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.27',
                    'id': 27,
                    'parent': 24,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 26 Name',
                    'role_number': 'SITE-ROLE-NUM-26'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 5'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.27.28',
                    'id': 28,
                    'parent': 27,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 27 Name',
                    'role_number': 'SITE-ROLE-NUM-27'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 6'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.27.28.29',
                    'id': 29,
                    'parent': 28,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 28 Name',
                    'role_number': 'SITE-ROLE-NUM-28'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 7'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.30',
                    'id': 30,
                    'parent': 24,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 29 Name',
                    'role_number': 'SITE-ROLE-NUM-29'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 8'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.31',
                    'id': 31,
                    'parent': 24,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 30 Name',
                    'role_number': 'SITE-ROLE-NUM-30'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 9'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.31.32',
                    'id': 32,
                    'parent': 31,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 31 Name',
                    'role_number': 'SITE-ROLE-NUM-31'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 10'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.31.33',
                    'id': 33,
                    'parent': 31,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 32 Name',
                    'role_number': 'SITE-ROLE-NUM-32'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 11'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.31.34',
                    'id': 34,
                    'parent': 31,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 33 Name',
                    'role_number': 'SITE-ROLE-NUM-33'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 12'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.31.34.35',
                    'id': 35,
                    'parent': 34,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 34 Name',
                    'role_number': 'SITE-ROLE-NUM-34'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 13'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.31.34.36',
                    'id': 36,
                    'parent': 34,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 35 Name',
                    'role_number': 'SITE-ROLE-NUM-35'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 14'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.37',
                    'id': 37,
                    'parent': 24,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 36 Name',
                    'role_number': 'SITE-ROLE-NUM-36'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 15'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.37.38',
                    'id': 38,
                    'parent': 37,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 37 Name',
                    'role_number': 'SITE-ROLE-NUM-37'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 16'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.37.38.39',
                    'id': 39,
                    'parent': 38,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 38 Name',
                    'role_number': 'SITE-ROLE-NUM-38'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 17'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.40',
                    'id': 40,
                    'parent': 24,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 39 Name',
                    'role_number': 'SITE-ROLE-NUM-39'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_2_approve_assets 18'] = {
    'data': {
        'update_reservation_view': {
            'returning': [
                {
                    'approval_status': 'Approved',
                    'approved': True,
                    'full_path': '1.24.40.41',
                    'id': 41,
                    'parent': 40,
                    'project_id': 2,
                    'reservable': True,
                    'reserved': True,
                    'role_name': 'Asset Number 40 Name',
                    'role_number': 'SITE-ROLE-NUM-40'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_3_add_new_roles 1'] = {
    'data': {
        'insert_reconciliation_view': {
            'returning': [
                None
            ]
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 140,
                    'line': 2
                }
            ],
            'message': 'Cannot return null for non-nullable field ReconViewType.asset_exists.',
            'path': [
                'insert_reconciliation_view',
                'returning',
                0,
                'asset_exists'
            ]
        }
    ]
}

snapshots['APITestCase::test_3_add_new_roles 2'] = {
    'data': {
        'insert_reconciliation_view': {
            'returning': [
                None
            ]
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 140,
                    'line': 2
                }
            ],
            'message': 'Cannot return null for non-nullable field ReconViewType.asset_exists.',
            'path': [
                'insert_reconciliation_view',
                'returning',
                0,
                'asset_exists'
            ]
        }
    ]
}

snapshots['APITestCase::test_3_add_new_roles 3'] = {
    'data': {
        'insert_reconciliation_view': {
            'returning': [
                None
            ]
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 140,
                    'line': 2
                }
            ],
            'message': 'Cannot return null for non-nullable field ReconViewType.asset_exists.',
            'path': [
                'insert_reconciliation_view',
                'returning',
                0,
                'asset_exists'
            ]
        }
    ]
}

snapshots['APITestCase::test_4_change_parent 1'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 31,
                    'asset_missing_from_registry': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-30',
                    'full_path': '11.34.41',
                    'id': 41,
                    'parent': 34,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_exists': True,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 30 Name',
                    'role_number': 'SITE-ROLE-NUM-30'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_4_change_parent 2'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 32,
                    'asset_missing_from_registry': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-31',
                    'full_path': '11.34.42',
                    'id': 42,
                    'parent': 34,
                    'parent_changed': True,
                    'project_id': 2,
                    'role_changed': False,
                    'role_exists': True,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 31 Name',
                    'role_number': 'SITE-ROLE-NUM-31'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_4_change_parent 3'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 33,
                    'asset_missing_from_registry': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-32',
                    'full_path': '11.34.43',
                    'id': 43,
                    'parent': 34,
                    'parent_changed': True,
                    'project_id': 2,
                    'role_changed': False,
                    'role_exists': True,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 32 Name',
                    'role_number': 'SITE-ROLE-NUM-32'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_4_change_parent 4'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 34,
                    'asset_missing_from_registry': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-33',
                    'full_path': '11.34.44',
                    'id': 44,
                    'parent': 34,
                    'parent_changed': True,
                    'project_id': 2,
                    'role_changed': False,
                    'role_exists': True,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 33 Name',
                    'role_number': 'SITE-ROLE-NUM-33'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_4_change_parent 5'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 35,
                    'asset_missing_from_registry': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-34',
                    'full_path': '11.34.45',
                    'id': 45,
                    'parent': 34,
                    'parent_changed': True,
                    'project_id': 2,
                    'role_changed': False,
                    'role_exists': True,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 34 Name',
                    'role_number': 'SITE-ROLE-NUM-34'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_4_change_parent 6'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 36,
                    'asset_missing_from_registry': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-35',
                    'full_path': '11.34.46',
                    'id': 46,
                    'parent': 34,
                    'parent_changed': True,
                    'project_id': 2,
                    'role_changed': False,
                    'role_exists': True,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 35 Name',
                    'role_number': 'SITE-ROLE-NUM-35'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_4_revert_parent 1'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 35,
                    'asset_missing_from_registry': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-34',
                    'full_path': '11.34.44.45',
                    'id': 45,
                    'parent': 44,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_exists': True,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 34 Name',
                    'role_number': 'SITE-ROLE-NUM-34'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_4_revert_parent 2'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 36,
                    'asset_missing_from_registry': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-35',
                    'full_path': '11.34.44.46',
                    'id': 46,
                    'parent': 44,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_exists': True,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 35 Name',
                    'role_number': 'SITE-ROLE-NUM-35'
                }
            ]
        }
    }
}

snapshots['APITestCase::test_5_unassign_assets 1'] = {
    'data': {
        'update_reconciliation_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '406:Operation Failed:',
            'path': [
                'update_reconciliation_view'
            ]
        }
    ]
}

snapshots['APITestCase::test_5_unassign_assets 2'] = {
    'data': {
        'update_reconciliation_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '406:Operation Failed:',
            'path': [
                'update_reconciliation_view'
            ]
        }
    ]
}

snapshots['APITestCase::test_5_unassign_assets 3'] = {
    'data': {
        'update_reconciliation_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '406:Operation Failed:',
            'path': [
                'update_reconciliation_view'
            ]
        }
    ]
}

snapshots['APITestCase::test_5_unassign_assets 4'] = {
    'data': {
        'update_reconciliation_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '406:Operation Failed:',
            'path': [
                'update_reconciliation_view'
            ]
        }
    ]
}

snapshots['APITestCase::test_6_reassign_assets 1'] = {
    'data': {
        'update_unassigned_assets': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '''relation "unassigned_assets" does not exist
LINE 1: ..._registry", "unassigned_assets"."project_id" FROM "unassigne...
                                                             ^
''',
            'path': [
                'update_unassigned_assets'
            ]
        }
    ]
}

snapshots['APITestCase::test_6_reassign_assets 2'] = {
    'data': {
        'update_unassigned_assets': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '''relation "unassigned_assets" does not exist
LINE 1: ..._registry", "unassigned_assets"."project_id" FROM "unassigne...
                                                             ^
''',
            'path': [
                'update_unassigned_assets'
            ]
        }
    ]
}
