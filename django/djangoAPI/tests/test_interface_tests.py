"""
Initializes the Database with test data and then interface tests are executed to check usability

TODO Check inputs of invalid data (from business rule sense)
"""
from snapshottest import TestCase
from graphene.test import Client
from djangoAPI.initialize import (clean_up_incrementers,
                                  fill_database_test_data, parse_avantis_data,
                                  run_sql_scripts)
from djangoAPI.graphql.schema import schema

RESERVATION_RETURN = 'returning {approval_status approved full_path id parent project_id reservable reserved role_name role_number}'
ROLE_ASSET_RETURN = 'returning {approved asset_exists asset_id asset_missing_from_registry asset_serial_number full_path id parent parent_changed project_id role_changed role_exists role_missing_from_registry role_name role_number role_new role_disposed designer_planned_action_type_tbl_id role_link asset_new}'
UNASSIGNED_RETURN = 'returning {asset_missing_from_registry asset_serial_number id project_id installation_stage_id uninstallation_stage_id asset_exists asset_new}'


class MetaHeader():
    def __init__(self, meta):
        self.META = meta


def initialization():
    run_sql_scripts()
    fill_database_test_data()
    parse_avantis_data()
    clean_up_incrementers()


class SystemTests(TestCase):
    """
    All tests required for the system
    Since a blank database is required for the test the initialization function must be used
    Most tests ensures standard usability, edge case testing will be added on as they are discovered
    """
    initialization()

    def test_01_reserve_assets(self):
        """
        Reserve some assets
        User: Tony, Group: 2, View: Reservation, Type: Standard Use Test
        """
        client = Client(schema)
        reserve_list = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
        for reserve in reserve_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_reservation_view(_set: { reserved: true}, where: {id: {_eq: %d}}) {%s
                }}''' % (reserve, RESERVATION_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_02_approve_assets(self):
        """
        Approve previously reserved assets
        User: Tony, Group: 2, View: Reservation, Type: Standard Use Test
        """
        client = Client(schema)
        reserve_list = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
        for reserve in reserve_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_reservation_view(_set: { approved: true}, where: {id: {_eq: %d}}) {%s
                }}''' % (reserve, RESERVATION_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_03_add_new_roles_w_asset(self):
        """
        Add roles with assets
        User: Tony, Group: 2, View: Reconciliation, Type: Standard Use Test
        """
        client = Client(schema)
        add_list = ['role_asset_1', 'role_asset_2', 'role_asset_3'] # 61-51, 62-52, 63-53
        for add in add_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                insert_reconciliation_view(objects: { role_number: "%s", role_name: "%s", parent: %d, asset_serial_number: "%s-serial-number"}) {%s
                }}''' % (add, add+' name', 34, add, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_04_0_change_parent(self):
        """
        Change parents of roles
        User: Tony, Group: 2, View: Reconciliation, Type: Standard Use Test
        """
        client = Client(schema)
        change_list = [41, 42, 43, 44, 45, 46]
        for change in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_reconciliation_view(_set: { parent: %d}, where: {id: {_eq: %d}}) {%s
                }}''' % (34, change, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_04_1_revert_parent(self):
        """
        Change parents of roles back (test parent_changed)
        User: Tony, Group: 2, View: Reconciliation, Type: Standard Use Test
        """
        client = Client(schema)
        change_list = [45, 46]
        for change in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_reconciliation_view(_set: { parent: %d}, where: { id: {_eq: %d}}) {%s
                }}''' % (44, change, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_05_unassign_assets(self): #TODO fix returns
        """
        Remove some assets from their roles
        User: Tony, Group: 2, View: Reconciliation, Type: Standard Use Test
        """
        client = Client(schema)
        change_list = [37, 38, 39, 40]
        for change in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_reconciliation_view(_set: { asset_id: %d}, where: {id: {_eq: %d}}) {%s
                }}''' % (change, 0, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_06_reassign_assets(self):
        """
        Switch up the assets role
        User: Tony, Group: 2, View: reconciliation_unassigned_asset, Type: Standard Use Test
        """
        client = Client(schema)
        change_list = [[47, 38], [48, 37]]
        for change in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_reconciliation_unassigned_asset_view(_set: { role_id: %d}, where: {id: {_eq: %d}}) {%s
                }}''' % (change[0], change[1], UNASSIGNED_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_07_add_role_only(self):
        """
        Add roles without assets
        User: Tony, Group: 2, View: Reconciliation, Type: Standard Use Test
        """
        client = Client(schema)
        add_list = ['role_only_1', 'role_only_2', 'role_only_3'] # 64, 65, 66
        for add in add_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                insert_reconciliation_view(objects: { role_number: "%s", role_name: "%s", parent: %d}) {%s
                }}''' % (add, add+' name', 34, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_08_add_asset_to_role(self):
        """
        Add new assets to roles
        User: Tony, Group: 2, View: Reconciliation, Type: Standard Use Test
        """
        client = Client(schema)
        add_list = ['asset_only_1', 'asset_only_2', 'asset_only_3']  # 54, 55, 56
        role_list = [49, 64, 65]
        for i, add in enumerate(add_list):
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                insert_reconciliation_view(objects: { asset_serial_number: "%s", id: %d}) {%s
                }}''' % (add, role_list[i], ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_09_0_non_existant_entities(self): # TODO fix return
        """
        Marks some entities as none existant (will also orphan some children)
        User: Tony, Group: 2, View: Reconciliation, Type: Standard Use Test
        """
        client = Client(schema)
        change_list = [34, 13, 16, 36]  # 13 / 16 should return errors about not being reserved
        for item in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                delete_reconciliation_view(where: { id: {_eq: %d}}) {%s
                }}''' % (item, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_09_1_non_existant_assets(self): 
        """
        Marks some assets as none existant
        User: Tony, Group: 2, View: Reconciliation, Type: Standard Use Test
        """
        client = Client(schema)
        change_list = [56, 63, 37]
        for item in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                delete_reconciliation_view(where: { asset_id: {_eq: %d}}) {%s
                }}''' % (item, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_10_orphan_census(self):
        """
        Query the reconciliation_orphan_view to ensure orphans have been properly created
        User: Tony, Group: 2, View: reconciliation_orphan_view, Type: Confirmation Test
        """
        # TODO all queries currently go through hasura so it does not exist
        pass

    def test_11_bring_back_non_existant_entities(self):
        """
        Brings entities marked as non existant back to reconciliation view
        User: Tony, Group: 2, View: garbage_can_reconciliation_view, Type: Standard Use Test
        """
        client = Client(schema) # TODO returns
        change_list = [34, 13, 16, 36]  # 13 / 16 should return errors about not being reserved
        for change in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_garbage_can_reconciliation_view(_set: { parent: %d}, where: {id: {_eq: %d}}) {%s
                }}''' % (33, change, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_12_delete_orphans(self):
        """
        Moves some orphan roles to the garbage
        User: Tony, Group: 2, View: reconciliation_orphan_view, Type: Standard Use Test
        """
        client = Client(schema) # TODO returns
        change_list = [40, 37, 41, 47, 50]
        for item in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                delete_reconciliation_orphan_view(where: { id: {_eq: %d}}) {%s
                }}''' % (item, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_13_assign_parent_to_orphans(self):
        """
        User: Tony, Group: 2, View: reconciliation_orphan_view, Type: Standard Use Test
        """
        client = Client(schema) # TODO returns
        change_list = [50, 35, 38, 61, 62, 64, 65]
        for change in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_reconciliation_orphan_view(_set: { parent: %d}, where: {id: {_eq: %d}}) {%s
                }}''' % (33, change, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_14_create_unassigned_asset(self):
        """
        User: Tony, Group: 2, View: reconciliation_unassigned_asset_view, Type: Standard Use Test
        """
        client = Client(schema)
        add_list = ['unasset_only_1', 'unasset_only_2', 'unasset_only_3']  # 57, 58, 59
        for i, add in enumerate(add_list):
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                insert_reconciliation_unassigned_asset_view(objects: { asset_serial_number: "%s" }) {%s
                }}''' % (add, UNASSIGNED_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_15_delete_unassigned_asset(self):
        """
        User: Tony, Group: 2, View: reconciliation_unassigned_asset_view, Type: Standard Use Test
        """
        client = Client(schema) # TODO returns 
        add_list = [58, 59, 39, 40]
        for i, add in enumerate(add_list):
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                delete_reconciliation_unassigned_asset_view(where: { id: {_eq: %d} }) {%s
                }}''' % (add, UNASSIGNED_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_16_assign_unassigned_asset(self):
        """
        User: Tony, Group: 2, View: reconciliation_unassigned_view, Type: Standard Use Test
        """
        client = Client(schema)
        add_list = [[47, 38], [48, 37]]  # TODO newly created and existing
        for add in add_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_garbage_can_asset_view(_set: { role_id: %d}, where: {id: {_eq: %d}}) {%s
                }}''' % (add[0], add[1], UNASSIGNED_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    # change view tests
    def test_17_create_changed_role_w_asset(self):
        """
        User: Tony, Group: 2, View: change_view, Type: Standard Use Test
        """
        client = Client(schema)
        # id, asset_id [[67, 57], [68, 58], [69, 59]]
        add_list = ['new_role_asset_1', 'new_role_asset_2', 'new_role_asset_3']
        for i, add in enumerate(add_list):
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                insert_change_view(objects: { role_number: "%s", role_name: "%s", parent: %d, asset_serial_number: "%s-serial-number"}) {%s
                }}''' % (add, add+' name', 34, add, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_18_change_parent(self):
        """
        Change parents of roles
        User: Tony, Group: 2, View: change_view, Type: Standard Use Test
        """
        client = Client(schema)
        change_list = [41, 42, 43, 44, 45, 46, 68, 69]  # TODO
        for change in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_change_view(_set: { parent: %d}, where: {id: {_eq: %d}}) {%s
                }}''' % (67, change, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_19_revert_parent(self):
        """
        Change parents of roles back (test parent_changed)
        User: Tony, Group: 2, View: change_view, Type: Standard Use Test
        """
        client = Client(schema)
        change_list = [45, 46]  # TODO
        for change in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_change_view(_set: { parent: %d}, where: { id: {_eq: %d}}) {%s
                }}''' % (44, change, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_20_unassign_assets(self):
        """
        Remove some assets from their roles
        User: Tony, Group: 2, View: change_view, Type: Standard Use Test
        """
        client = Client(schema)
        change_list = [37, 38, 39, 40]
        for change in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_change_view(_set: { asset_id: %d}, where: {id: {_eq: %d}}) {%s
                }}''' % (change, 0, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_21_reassign_assets(self):
        """
        Switch up the assets role
        User: Tony, Group: 2, View: change_unassigned_asset, Type: Standard Use Test
        """
        client = Client(schema)
        change_list = [[47, 38], [48, 37]]  # TODO
        for change in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_change_unassigned_asset_view(_set: { role_id: %d}, where: {id: {_eq: %d}}) {%s
                }}''' % (change[0], change[1], UNASSIGNED_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_22_add_role_only(self):
        """
        Add roles without assets
        User: Tony, Group: 2, View: change, Type: Standard Use Test
        """
        client = Client(schema)
        add_list = ['new_role_only_1', 'new_role_only_2', 'new_role_only_3']
        # id [[70, 71, 72]]
        for add in add_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                insert_change_view(objects: { role_number: "%s", role_name: "%s", parent: %d}) {%s
                }}''' % (add, add+' name', 44, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_23_add_asset_to_role(self):
        """
        Add new assets to roles
        User: Tony, Group: 2, View: change, Type: Standard Use Test
        """
        client = Client(schema)
        add_list = ['new_asset_only_1', 'new_asset_only_2', 'new_asset_only_3']
        role_list = [49, 64, 65]  # TODO
        for i, add in enumerate(add_list):
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                insert_change_view(objects: { asset_serial_number: "%s", id: %d}) {%s
                }}''' % (add, role_list[i], ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_24_non_existant_entities(self):
        """
        Marks some entities as none existant (will also orphan some children) #TODO change orphan view is deprecated
        User: Tony, Group: 2, View: change, Type: Standard Use Test
        """
        client = Client(schema)
        change_list = [72, 67]  # TODO
        for item in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                delete_change_view(where: { id: {_eq: %d}}) {%s
                }}''' % (item, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_25_orphan_census(self):  # change orphan view is deprecated
        """
        Query the reconciliation_orphan_view to ensure orphans have been properly created
        User: Tony, Group: 2, View: change_orphan_view, Type: Confirmation Test
        """
        # TODO all queries currently go through hasura so it does not exist
        pass

    def test_26_bring_back_non_existant_entities(self):
        """
        Brings entities marked as non existant back to change view
        User: Tony, Group: 2, View: update_dumpster_change_view, Type: Standard Use Test
        """
        # TODO this specific mutation does not exist
        client = Client(schema)
        change_list = [34, 13, 16, 36]  # TODO
        for change in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_dumpster_change_view(_set: { parent: %d}, where: {id: {_eq: %d}}) {%s
                }}''' % (33, change, ROLE_ASSET_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_27_delete_orphans(self):  # change orphan view is deprecated
        """
        Moves some orphan roles to the garbage
        User: Tony, Group: 2, View: change_orphan_view, Type: Standard Use Test
        """
        pass
        # client = Client(schema)
        # change_list = [40, 37, 41, 47, 50]  # TODO
        # for item in change_list:
        #     self.assertMatchSnapshot(client.execute('''mutation MyMutation {
        #         delete_change_orphan_view(where: { id: {_eq: %d}}) {%s
        #         }}''' % (item, ROLE_ASSET_RETURN),
        #         context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_28_assign_parent_to_orphans(self):  # change orphan view is deprecated
        """
        User: Tony, Group: 2, View: change_orphan_view, Type: Standard Use Test
        """
        pass
        # client = Client(schema)
        # change_list = [50]  # TODO
        # for change in change_list:
        #     self.assertMatchSnapshot(client.execute('''mutation MyMutation {
        #         update_change_orphan_view(_set: { parent: %d}, where: {id: {_eq: %d}}) {%s
        #         }}''' % (33, change, ROLE_ASSET_RETURN),
        #         context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_29_create_unassigned_asset(self):
        """
        User: Tony, Group: 2, View: change_unassigned_asset_view, Type: Standard Use Test
        """
        client = Client(schema)
        add_list = ['new_unasset_only_1', 'new_unasset_only_2', 'new_unasset_only_3']
        for i, add in enumerate(add_list):
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                insert_change_unassigned_asset_view(objects: { asset_serial_number: "%s" }) {%s
                }}''' % (add, UNASSIGNED_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_30_delete_unassigned_asset(self):
        """
        User: Tony, Group: 2, View: change_unassigned_asset_view, Type: Standard Use Test
        """
        client = Client(schema)
        add_list = [69, 420, 69]  # TODO newly created and existing
        for i, add in enumerate(add_list):
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                delete_change_unassigned_asset_view(where: { id: {_eq: %d} }) {%s
                }}''' % (add, UNASSIGNED_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_31_assign_unassigned_asset(self):
        """
        User: Tony, Group: 2, View: dumpster_asset_view, Type: Standard Use Test
        """
        client = Client(schema)
        add_list = [[47, 38], [48, 37]]  # TODO newly created and existing
        for add in add_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_dumpster_asset_view(_set: { role_id: %d}, where: {id: {_eq: %d}}) {%s
                }}''' % (add[0], add[1], UNASSIGNED_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))
