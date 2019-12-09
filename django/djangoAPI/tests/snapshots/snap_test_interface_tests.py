# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['SystemTests::test_01_reserve_assets 1'] = {
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

snapshots['SystemTests::test_01_reserve_assets 2'] = {
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

snapshots['SystemTests::test_01_reserve_assets 3'] = {
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

snapshots['SystemTests::test_01_reserve_assets 4'] = {
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

snapshots['SystemTests::test_01_reserve_assets 5'] = {
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

snapshots['SystemTests::test_01_reserve_assets 6'] = {
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

snapshots['SystemTests::test_01_reserve_assets 7'] = {
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

snapshots['SystemTests::test_01_reserve_assets 8'] = {
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

snapshots['SystemTests::test_01_reserve_assets 9'] = {
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

snapshots['SystemTests::test_01_reserve_assets 10'] = {
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

snapshots['SystemTests::test_01_reserve_assets 11'] = {
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

snapshots['SystemTests::test_01_reserve_assets 12'] = {
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

snapshots['SystemTests::test_01_reserve_assets 13'] = {
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

snapshots['SystemTests::test_01_reserve_assets 14'] = {
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

snapshots['SystemTests::test_01_reserve_assets 15'] = {
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

snapshots['SystemTests::test_01_reserve_assets 16'] = {
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

snapshots['SystemTests::test_01_reserve_assets 17'] = {
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

snapshots['SystemTests::test_01_reserve_assets 18'] = {
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

snapshots['SystemTests::test_02_approve_assets 1'] = {
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

snapshots['SystemTests::test_02_approve_assets 2'] = {
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

snapshots['SystemTests::test_02_approve_assets 3'] = {
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

snapshots['SystemTests::test_02_approve_assets 4'] = {
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

snapshots['SystemTests::test_02_approve_assets 5'] = {
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

snapshots['SystemTests::test_02_approve_assets 6'] = {
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

snapshots['SystemTests::test_02_approve_assets 7'] = {
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

snapshots['SystemTests::test_02_approve_assets 8'] = {
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

snapshots['SystemTests::test_02_approve_assets 9'] = {
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

snapshots['SystemTests::test_02_approve_assets 10'] = {
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

snapshots['SystemTests::test_02_approve_assets 11'] = {
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

snapshots['SystemTests::test_02_approve_assets 12'] = {
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

snapshots['SystemTests::test_02_approve_assets 13'] = {
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

snapshots['SystemTests::test_02_approve_assets 14'] = {
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

snapshots['SystemTests::test_02_approve_assets 15'] = {
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

snapshots['SystemTests::test_02_approve_assets 16'] = {
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

snapshots['SystemTests::test_02_approve_assets 17'] = {
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

snapshots['SystemTests::test_02_approve_assets 18'] = {
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

snapshots['SystemTests::test_03_add_new_roles_w_asset 1'] = {
    'data': {
        'insert_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': None,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': None,
                    'designer_planned_action_type_tbl_id': None,
                    'full_path': '11.34.61',
                    'id': 61,
                    'parent': 34,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': None,
                    'role_missing_from_registry': True,
                    'role_name': 'role_asset_1 name',
                    'role_new': False,
                    'role_number': 'role_asset_1'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_03_add_new_roles_w_asset 2'] = {
    'data': {
        'insert_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': None,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': None,
                    'designer_planned_action_type_tbl_id': None,
                    'full_path': '11.34.62',
                    'id': 62,
                    'parent': 34,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': None,
                    'role_missing_from_registry': True,
                    'role_name': 'role_asset_2 name',
                    'role_new': False,
                    'role_number': 'role_asset_2'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_03_add_new_roles_w_asset 3'] = {
    'data': {
        'insert_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': None,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': None,
                    'designer_planned_action_type_tbl_id': None,
                    'full_path': '11.34.63',
                    'id': 63,
                    'parent': 34,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': None,
                    'role_missing_from_registry': True,
                    'role_name': 'role_asset_3 name',
                    'role_new': False,
                    'role_number': 'role_asset_3'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_04_0_change_parent 1'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 31,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-30',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.34.41',
                    'id': 41,
                    'parent': 34,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 41,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 30 Name',
                    'role_new': False,
                    'role_number': 'SITE-ROLE-NUM-30'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_04_0_change_parent 2'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 32,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-31',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.34.42',
                    'id': 42,
                    'parent': 34,
                    'parent_changed': True,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 42,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 31 Name',
                    'role_new': False,
                    'role_number': 'SITE-ROLE-NUM-31'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_04_0_change_parent 3'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 33,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-32',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.34.43',
                    'id': 43,
                    'parent': 34,
                    'parent_changed': True,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 43,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 32 Name',
                    'role_new': False,
                    'role_number': 'SITE-ROLE-NUM-32'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_04_0_change_parent 4'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 34,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-33',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.34.44',
                    'id': 44,
                    'parent': 34,
                    'parent_changed': True,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 44,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 33 Name',
                    'role_new': False,
                    'role_number': 'SITE-ROLE-NUM-33'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_04_0_change_parent 5'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 35,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-34',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.34.45',
                    'id': 45,
                    'parent': 34,
                    'parent_changed': True,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 45,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 34 Name',
                    'role_new': False,
                    'role_number': 'SITE-ROLE-NUM-34'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_04_0_change_parent 6'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 36,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-35',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.34.46',
                    'id': 46,
                    'parent': 34,
                    'parent_changed': True,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 46,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 35 Name',
                    'role_new': False,
                    'role_number': 'SITE-ROLE-NUM-35'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_04_1_revert_parent 1'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 35,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-34',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.34.44.45',
                    'id': 45,
                    'parent': 44,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 45,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 34 Name',
                    'role_new': False,
                    'role_number': 'SITE-ROLE-NUM-34'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_04_1_revert_parent 2'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 36,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-35',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.34.44.46',
                    'id': 46,
                    'parent': 44,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 46,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 35 Name',
                    'role_new': False,
                    'role_number': 'SITE-ROLE-NUM-35'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_05_unassign_assets 1'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_05_unassign_assets 2'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_05_unassign_assets 3'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_05_unassign_assets 4'] = {
    'data': {
        'update_reconciliation_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_06_reassign_assets 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': 'Cannot query field "update_reconciliation_unassigned_assets" on type "Mutations". Did you mean "update_reconciliation_unassigned_asset_view", "delete_reconciliation_unassigned_asset_view", "insert_reconciliation_unassigned_asset_view", "update_reconciliation_orphan_view" or "update_reconciliation_view"?'
        }
    ]
}

snapshots['SystemTests::test_06_reassign_assets 2'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': 'Cannot query field "update_reconciliation_unassigned_assets" on type "Mutations". Did you mean "update_reconciliation_unassigned_asset_view", "delete_reconciliation_unassigned_asset_view", "insert_reconciliation_unassigned_asset_view", "update_reconciliation_orphan_view" or "update_reconciliation_view"?'
        }
    ]
}

snapshots['SystemTests::test_07_add_role_only 1'] = {
    'data': {
        'insert_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': None,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': None,
                    'designer_planned_action_type_tbl_id': None,
                    'full_path': '11.34.64',
                    'id': 64,
                    'parent': 34,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': None,
                    'role_missing_from_registry': True,
                    'role_name': 'role_only_1 name',
                    'role_new': False,
                    'role_number': 'role_only_1'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_07_add_role_only 2'] = {
    'data': {
        'insert_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': None,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': None,
                    'designer_planned_action_type_tbl_id': None,
                    'full_path': '11.34.65',
                    'id': 65,
                    'parent': 34,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': None,
                    'role_missing_from_registry': True,
                    'role_name': 'role_only_2 name',
                    'role_new': False,
                    'role_number': 'role_only_2'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_07_add_role_only 3'] = {
    'data': {
        'insert_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': None,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': None,
                    'designer_planned_action_type_tbl_id': None,
                    'full_path': '11.34.66',
                    'id': 66,
                    'parent': 34,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': None,
                    'role_missing_from_registry': True,
                    'role_name': 'role_only_3 name',
                    'role_new': False,
                    'role_number': 'role_only_3'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_08_add_asset_to_role 1'] = {
    'data': {
        'insert_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 51,
                    'asset_missing_from_registry': True,
                    'asset_new': False,
                    'asset_serial_number': 'asset_only_1',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.34.47.48.49',
                    'id': 49,
                    'parent': 48,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 49,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 38 Name',
                    'role_new': False,
                    'role_number': 'SITE-ROLE-NUM-38'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_08_add_asset_to_role 2'] = {
    'data': {
        'insert_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 52,
                    'asset_missing_from_registry': True,
                    'asset_new': False,
                    'asset_serial_number': 'asset_only_2',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.34.64',
                    'id': 64,
                    'parent': 34,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 64,
                    'role_missing_from_registry': True,
                    'role_name': 'role_only_1 name',
                    'role_new': False,
                    'role_number': 'role_only_1'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_08_add_asset_to_role 3'] = {
    'data': {
        'insert_reconciliation_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 53,
                    'asset_missing_from_registry': True,
                    'asset_new': False,
                    'asset_serial_number': 'asset_only_3',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.34.65',
                    'id': 65,
                    'parent': 34,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 65,
                    'role_missing_from_registry': True,
                    'role_name': 'role_only_2 name',
                    'role_new': False,
                    'role_number': 'role_only_2'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_09_non_existant_entities 1'] = {
    'data': {
        'delete_reconciliation_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_09_non_existant_entities 2'] = {
    'data': {
        'delete_reconciliation_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '4:Asset Reserved by Another Project:',
            'path': [
                'delete_reconciliation_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_09_non_existant_entities 3'] = {
    'data': {
        'delete_reconciliation_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '4:Asset Reserved by Another Project:',
            'path': [
                'delete_reconciliation_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_09_non_existant_entities 4'] = {
    'data': {
        'delete_reconciliation_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_11_bring_back_non_existant_entities 1'] = {
    'data': {
        'update_garbage_can_reconciliation_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_11_bring_back_non_existant_entities 2'] = {
    'data': {
        'update_garbage_can_reconciliation_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '302:Entity unreserved or reserved by another project:',
            'path': [
                'update_garbage_can_reconciliation_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_11_bring_back_non_existant_entities 3'] = {
    'data': {
        'update_garbage_can_reconciliation_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '302:Entity unreserved or reserved by another project:',
            'path': [
                'update_garbage_can_reconciliation_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_11_bring_back_non_existant_entities 4'] = {
    'data': {
        'update_garbage_can_reconciliation_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_12_delete_orphans 1'] = {
    'data': {
        'delete_reconciliation_orphan_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_12_delete_orphans 2'] = {
    'data': {
        'delete_reconciliation_orphan_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_12_delete_orphans 3'] = {
    'data': {
        'delete_reconciliation_orphan_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_12_delete_orphans 4'] = {
    'data': {
        'delete_reconciliation_orphan_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_12_delete_orphans 5'] = {
    'data': {
        'delete_reconciliation_orphan_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_13_assign_parent_to_orphans 1'] = {
    'data': {
        'update_reconciliation_orphan_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_14_create_unassigned_asset 1'] = {
    'data': {
        'insert_reconciliation_unassigned_asset_view': {
            'returning': [
                {
                    'asset_exists': True,
                    'asset_missing_from_registry': True,
                    'asset_new': False,
                    'asset_serial_number': 'unasset_only_1',
                    'id': 54,
                    'installation_stage_id': None,
                    'project_id': 2,
                    'uninstallation_stage_id': None
                }
            ]
        }
    }
}

snapshots['SystemTests::test_14_create_unassigned_asset 2'] = {
    'data': {
        'insert_reconciliation_unassigned_asset_view': {
            'returning': [
                {
                    'asset_exists': True,
                    'asset_missing_from_registry': True,
                    'asset_new': False,
                    'asset_serial_number': 'unasset_only_2',
                    'id': 55,
                    'installation_stage_id': None,
                    'project_id': 2,
                    'uninstallation_stage_id': None
                }
            ]
        }
    }
}

snapshots['SystemTests::test_14_create_unassigned_asset 3'] = {
    'data': {
        'insert_reconciliation_unassigned_asset_view': {
            'returning': [
                {
                    'asset_exists': True,
                    'asset_missing_from_registry': True,
                    'asset_new': False,
                    'asset_serial_number': 'unasset_only_3',
                    'id': 56,
                    'installation_stage_id': None,
                    'project_id': 2,
                    'uninstallation_stage_id': None
                }
            ]
        }
    }
}

snapshots['SystemTests::test_15_delete_unassigned_asset 1'] = {
    'data': {
        'delete_reconciliation_unassigned_asset_view': {
            'returning': [
                {
                    'asset_exists': True,
                    'asset_missing_from_registry': True,
                    'asset_new': False,
                    'asset_serial_number': 'unasset_only_3',
                    'id': 56,
                    'installation_stage_id': None,
                    'project_id': 2,
                    'uninstallation_stage_id': None
                }
            ]
        }
    }
}

snapshots['SystemTests::test_15_delete_unassigned_asset 2'] = {
    'data': {
        'delete_reconciliation_unassigned_asset_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': "E14: Asset cannot be found please refresh your View: {'asset_id': 69}",
            'path': [
                'delete_reconciliation_unassigned_asset_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_15_delete_unassigned_asset 3'] = {
    'data': {
        'delete_reconciliation_unassigned_asset_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': "E14: Asset cannot be found please refresh your View: {'asset_id': 420}",
            'path': [
                'delete_reconciliation_unassigned_asset_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_15_delete_unassigned_asset 4'] = {
    'data': {
        'delete_reconciliation_unassigned_asset_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': "E14: Asset cannot be found please refresh your View: {'asset_id': 69}",
            'path': [
                'delete_reconciliation_unassigned_asset_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_16_assign_unassigned_asset 1'] = {
    'data': {
        'update_garbage_can_asset_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '402:You are assigning an asset to a role that is marked as Non Existant:',
            'path': [
                'update_garbage_can_asset_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_16_assign_unassigned_asset 2'] = {
    'data': {
        'update_garbage_can_asset_view': {
            'returning': [
                {
                    'asset_exists': True,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-36',
                    'id': 37,
                    'installation_stage_id': None,
                    'project_id': 2,
                    'uninstallation_stage_id': None
                }
            ]
        }
    }
}

snapshots['SystemTests::test_17_create_changed_role_w_asset 1'] = {
    'data': {
        'insert_change_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 57,
                    'asset_missing_from_registry': False,
                    'asset_new': True,
                    'asset_serial_number': 'new_role_asset_1-serial-number',
                    'designer_planned_action_type_tbl_id': None,
                    'full_path': '11.29.31.32.33.34.67',
                    'id': 67,
                    'parent': 34,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 67,
                    'role_missing_from_registry': False,
                    'role_name': 'new_role_asset_1 name',
                    'role_new': True,
                    'role_number': 'new_role_asset_1'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_17_create_changed_role_w_asset 2'] = {
    'data': {
        'insert_change_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 58,
                    'asset_missing_from_registry': False,
                    'asset_new': True,
                    'asset_serial_number': 'new_role_asset_2-serial-number',
                    'designer_planned_action_type_tbl_id': None,
                    'full_path': '11.29.31.32.33.34.68',
                    'id': 68,
                    'parent': 34,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 68,
                    'role_missing_from_registry': False,
                    'role_name': 'new_role_asset_2 name',
                    'role_new': True,
                    'role_number': 'new_role_asset_2'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_17_create_changed_role_w_asset 3'] = {
    'data': {
        'insert_change_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 59,
                    'asset_missing_from_registry': False,
                    'asset_new': True,
                    'asset_serial_number': 'new_role_asset_3-serial-number',
                    'designer_planned_action_type_tbl_id': None,
                    'full_path': '11.29.31.32.33.34.69',
                    'id': 69,
                    'parent': 34,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 69,
                    'role_missing_from_registry': False,
                    'role_name': 'new_role_asset_3 name',
                    'role_new': True,
                    'role_number': 'new_role_asset_3'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_18_change_parent 1'] = {
    'data': {
        'update_change_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_18_change_parent 2'] = {
    'data': {
        'update_change_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 32,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-31',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.29.31.32.33.34.67.42',
                    'id': 42,
                    'parent': 67,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 42,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 31 Name',
                    'role_new': False,
                    'role_number': 'SITE-ROLE-NUM-31'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_18_change_parent 3'] = {
    'data': {
        'update_change_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 33,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-32',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.29.31.32.33.34.67.43',
                    'id': 43,
                    'parent': 67,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 43,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 32 Name',
                    'role_new': False,
                    'role_number': 'SITE-ROLE-NUM-32'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_18_change_parent 4'] = {
    'data': {
        'update_change_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 34,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-33',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.29.31.32.33.34.67.44',
                    'id': 44,
                    'parent': 67,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 44,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 33 Name',
                    'role_new': False,
                    'role_number': 'SITE-ROLE-NUM-33'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_18_change_parent 5'] = {
    'data': {
        'update_change_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 35,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-34',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.29.31.32.33.34.67.45',
                    'id': 45,
                    'parent': 67,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 45,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 34 Name',
                    'role_new': False,
                    'role_number': 'SITE-ROLE-NUM-34'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_18_change_parent 6'] = {
    'data': {
        'update_change_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 36,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-35',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.29.31.32.33.34.67.46',
                    'id': 46,
                    'parent': 67,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 46,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 35 Name',
                    'role_new': False,
                    'role_number': 'SITE-ROLE-NUM-35'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_18_change_parent 7'] = {
    'data': {
        'update_change_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 58,
                    'asset_missing_from_registry': False,
                    'asset_new': True,
                    'asset_serial_number': 'new_role_asset_2-serial-number',
                    'designer_planned_action_type_tbl_id': None,
                    'full_path': '11.29.31.32.33.34.67.68',
                    'id': 68,
                    'parent': 67,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 68,
                    'role_missing_from_registry': False,
                    'role_name': 'new_role_asset_2 name',
                    'role_new': True,
                    'role_number': 'new_role_asset_2'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_18_change_parent 8'] = {
    'data': {
        'update_change_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 59,
                    'asset_missing_from_registry': False,
                    'asset_new': True,
                    'asset_serial_number': 'new_role_asset_3-serial-number',
                    'designer_planned_action_type_tbl_id': None,
                    'full_path': '11.29.31.32.33.34.67.69',
                    'id': 69,
                    'parent': 67,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 69,
                    'role_missing_from_registry': False,
                    'role_name': 'new_role_asset_3 name',
                    'role_new': True,
                    'role_number': 'new_role_asset_3'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_19_revert_parent 1'] = {
    'data': {
        'update_change_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 35,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-34',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.29.31.32.33.34.67.44.45',
                    'id': 45,
                    'parent': 44,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 45,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 34 Name',
                    'role_new': False,
                    'role_number': 'SITE-ROLE-NUM-34'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_19_revert_parent 2'] = {
    'data': {
        'update_change_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': 36,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': 'ASN SITE-ROLE-NUM-35',
                    'designer_planned_action_type_tbl_id': 'c',
                    'full_path': '11.29.31.32.33.34.67.44.46',
                    'id': 46,
                    'parent': 44,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': 46,
                    'role_missing_from_registry': False,
                    'role_name': 'Asset Number 35 Name',
                    'role_new': False,
                    'role_number': 'SITE-ROLE-NUM-35'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_20_unassign_assets 1'] = {
    'data': {
        'update_change_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_20_unassign_assets 2'] = {
    'data': {
        'update_change_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_20_unassign_assets 3'] = {
    'data': {
        'update_change_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_20_unassign_assets 4'] = {
    'data': {
        'update_change_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_21_reassign_assets 1'] = {
    'data': {
        'update_change_unassigned_asset_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '603:You are assigning an asset to a role that is marked as Non Existant:',
            'path': [
                'update_change_unassigned_asset_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_21_reassign_assets 2'] = {
    'data': {
        'update_change_unassigned_asset_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '600:Another Asset is currently assigned to this role: ASN SITE-ROLE-NUM-36:',
            'path': [
                'update_change_unassigned_asset_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_22_add_role_only 1'] = {
    'data': {
        'insert_change_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': None,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': None,
                    'designer_planned_action_type_tbl_id': None,
                    'full_path': '11.29.31.32.33.34.67.44.70',
                    'id': 70,
                    'parent': 44,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': None,
                    'role_missing_from_registry': False,
                    'role_name': 'new_role_only_1 name',
                    'role_new': True,
                    'role_number': 'new_role_only_1'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_22_add_role_only 2'] = {
    'data': {
        'insert_change_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': None,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': None,
                    'designer_planned_action_type_tbl_id': None,
                    'full_path': '11.29.31.32.33.34.67.44.71',
                    'id': 71,
                    'parent': 44,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': None,
                    'role_missing_from_registry': False,
                    'role_name': 'new_role_only_2 name',
                    'role_new': True,
                    'role_number': 'new_role_only_2'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_22_add_role_only 3'] = {
    'data': {
        'insert_change_view': {
            'returning': [
                {
                    'approved': True,
                    'asset_exists': True,
                    'asset_id': None,
                    'asset_missing_from_registry': False,
                    'asset_new': False,
                    'asset_serial_number': None,
                    'designer_planned_action_type_tbl_id': None,
                    'full_path': '11.29.31.32.33.34.67.44.72',
                    'id': 72,
                    'parent': 44,
                    'parent_changed': False,
                    'project_id': 2,
                    'role_changed': False,
                    'role_disposed': False,
                    'role_exists': True,
                    'role_link': None,
                    'role_missing_from_registry': False,
                    'role_name': 'new_role_only_3 name',
                    'role_new': True,
                    'role_number': 'new_role_only_3'
                }
            ]
        }
    }
}

snapshots['SystemTests::test_23_add_asset_to_role 1'] = {
    'data': {
        'insert_change_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_23_add_asset_to_role 2'] = {
    'data': {
        'insert_change_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_23_add_asset_to_role 3'] = {
    'data': {
        'insert_change_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_24_non_existant_entities 1'] = {
    'data': {
        'delete_change_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_24_non_existant_entities 2'] = {
    'data': {
        'delete_change_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_26_bring_back_non_existant_entities 1'] = {
    'data': {
        'update_dumpster_change_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_26_bring_back_non_existant_entities 2'] = {
    'data': {
        'update_dumpster_change_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '302:Entity unreserved or reserved by another project:',
            'path': [
                'update_dumpster_change_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_26_bring_back_non_existant_entities 3'] = {
    'data': {
        'update_dumpster_change_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '302:Entity unreserved or reserved by another project:',
            'path': [
                'update_dumpster_change_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_26_bring_back_non_existant_entities 4'] = {
    'data': {
        'update_dumpster_change_view': {
            'returning': [
            ]
        }
    }
}

snapshots['SystemTests::test_29_create_unassigned_asset 1'] = {
    'data': {
        'insert_change_unassigned_asset_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '''26:Failed to Create New Asset:null value in column "final_project_asset_role_id_id" violates not-null constraint
DETAIL:  Failing row contains (63, null, 1).
:<class 'django.db.utils.IntegrityError'>''',
            'path': [
                'insert_change_unassigned_asset_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_29_create_unassigned_asset 2'] = {
    'data': {
        'insert_change_unassigned_asset_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '''26:Failed to Create New Asset:null value in column "final_project_asset_role_id_id" violates not-null constraint
DETAIL:  Failing row contains (64, null, 1).
:<class 'django.db.utils.IntegrityError'>''',
            'path': [
                'insert_change_unassigned_asset_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_29_create_unassigned_asset 3'] = {
    'data': {
        'insert_change_unassigned_asset_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '''26:Failed to Create New Asset:null value in column "final_project_asset_role_id_id" violates not-null constraint
DETAIL:  Failing row contains (65, null, 1).
:<class 'django.db.utils.IntegrityError'>''',
            'path': [
                'insert_change_unassigned_asset_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_30_delete_unassigned_asset 1'] = {
    'data': {
        'delete_change_unassigned_asset_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': "800:Asset does not exist:ProjectAssetRecordTbl matching query does not exist.:<class 'djangoAPI.models.ProjectAssetRecordTbl.DoesNotExist'>",
            'path': [
                'delete_change_unassigned_asset_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_30_delete_unassigned_asset 2'] = {
    'data': {
        'delete_change_unassigned_asset_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': "800:Asset does not exist:ProjectAssetRecordTbl matching query does not exist.:<class 'djangoAPI.models.ProjectAssetRecordTbl.DoesNotExist'>",
            'path': [
                'delete_change_unassigned_asset_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_30_delete_unassigned_asset 3'] = {
    'data': {
        'delete_change_unassigned_asset_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': "800:Asset does not exist:ProjectAssetRecordTbl matching query does not exist.:<class 'djangoAPI.models.ProjectAssetRecordTbl.DoesNotExist'>",
            'path': [
                'delete_change_unassigned_asset_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_31_assign_unassigned_asset 1'] = {
    'data': {
        'update_dumpster_asset_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '603:You are assigning an asset to a role that is marked as Non Existant:',
            'path': [
                'update_dumpster_asset_view'
            ]
        }
    ]
}

snapshots['SystemTests::test_31_assign_unassigned_asset 2'] = {
    'data': {
        'update_dumpster_asset_view': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 17,
                    'line': 2
                }
            ],
            'message': '600:Another Asset is currently assigned to this role: ASN SITE-ROLE-NUM-36:',
            'path': [
                'update_dumpster_asset_view'
            ]
        }
    ]
}
