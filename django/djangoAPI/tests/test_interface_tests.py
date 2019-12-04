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
RECONCILIATION_RETURN = 'returning {approved asset_exists asset_id asset_missing_from_registry asset_serial_number full_path id parent parent_changed project_id role_changed role_exists role_missing_from_registry role_name role_number}'
UNASSIGNED_RETURN = 'returning {asset_missing_from_registry asset_serial_number id project_id}'


class MetaHeader():
    def __init__(self, meta):
        self.META = meta


def initialization():
    run_sql_scripts()
    fill_database_test_data()
    parse_avantis_data()
    clean_up_incrementers()


class APITestCase(TestCase):

    initialization()

    def test_1_reserve_assets(self):
        """
        Some required information for making requests to graphql and rest
        """
        client = Client(schema)
        reserve_list = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
        for reserve in reserve_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_reservation_view(_set: { reserved: true}, where: {id: {_eq: %d}}) {%s
                }}''' % (reserve, RESERVATION_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_2_approve_assets(self):
        client = Client(schema)
        reserve_list = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
        for reserve in reserve_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_reservation_view(_set: { approved: true}, where: {id: {_eq: %d}}) {%s
                }}''' % (reserve, RESERVATION_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_3_add_new_roles(self):
        client = Client(schema)
        add_list = ['asset_1', 'asset_2', 'asset_3']
        for add in add_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                insert_reconciliation_view(objects: { role_number: "%s", role_name: "%s", parent: %d}) {%s
                }}''' % (add, add+' name', 34, RECONCILIATION_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_4_change_parent(self):
        client = Client(schema)
        change_list = [41, 42, 43, 44, 45, 46]
        for change in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_reconciliation_view(_set: { parent: %d}, where: {id: {_eq: %d}}) {%s
                }}''' % (34, change, RECONCILIATION_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_4_revert_parent(self):
        client = Client(schema)
        change_list = [45, 46]
        for change in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_reconciliation_view(_set: {parent: %d}, where: {id: {_eq: %d}}) {%s
                }}''' % (44, change, RECONCILIATION_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_5_unassign_assets(self):
        client = Client(schema)
        change_list = [37, 38, 39, 40]
        for change in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_reconciliation_view(_set: { asset_id: %d}, where: {id: {_eq: %d}}) {%s
                }}''' % (change, 0, RECONCILIATION_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))

    def test_6_reassign_assets(self):
        client = Client(schema)
        change_list = [[47, 38], [48, 37], [61, 39]]
        for change in change_list:
            self.assertMatchSnapshot(client.execute('''mutation MyMutation {
                update_unassigned_assets(_set: { role_id: %d}, where: {id: {_eq: %d}}) {%s
                }}''' % (change[0], change[1], UNASSIGNED_RETURN),
                context=MetaHeader({'HTTP_X_USERNAME': 'tony.huang', 'HTTP_X_PROJECT': 2})))
