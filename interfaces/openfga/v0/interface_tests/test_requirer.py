# Copyright 2023 Canonical
# See LICENSE file for licensing details.
from interface_tester import Tester
from scenario import Relation, State


def test_no_data_on_created(output_state: State):
    # nothing happens on created: databags are empty
    t = Tester()
    t.run('openfga-relation-created')
    t.assert_relation_data_empty()


def test_no_data_on_joined(output_state: State):
    # nothing happens on joined: databags are empty
    t = Tester()
    t.run('openfga-relation-joined')
    t.assert_relation_data_empty()


def test_data_published_on_changed_remote_valid(output_state: State):
    t = Tester(State(
        relations=[Relation(
            endpoint='openfga',
            interface='openfga',
            remote_app_name='remote',
            remote_app_data={
                'address': '10.10.4.1',
                'port': "8080",
                'scheme': 'https',
                'token_secret_id': "test_token_secret",
                'store_id': '01GK13VYZK62Q1T0X55Q2BHYD6',
            }
        )]
    ))
    t.run('openfga-relation-changed')
    t.assert_schema_valid()
