"""
Test to make sure that model instances can be initialized correctly
"""

from django.test import TestCase
from djangoAPI.initialize import (clean_up_incrementers,
                                  fill_database_test_data, parse_avantis_data,
                                  run_sql_scripts, update_hasura_schema)


class test_everything(TestCase):
    """
    This is an interface test

    1. data can be imported

    2. Role and asset data through graphql

    3. Project information through graphql and rest
    """

    def test_initialization(self):
        run_sql_scripts()
        fill_database_test_data()
        parse_avantis_data()
        clean_up_incrementers()
