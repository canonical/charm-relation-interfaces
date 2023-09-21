# Copyright 2023 Canonical
# See LICENSE file for licensing details.
from interface_tester import Tester
from scenario import Relation, State


def test_no_data_on_created():
    # nothing happens on created: databags are empty
    t = Tester()
    t.run('openfga-relation-created')
    t.assert_relation_data_empty()


def test_no_data_on_joined():
    # nothing happens on joined: databags are empty
    t = Tester()
    t.run('openfga-relation-joined')
    t.assert_relation_data_empty()


def test_data_published_on_changed_remote_valid():
    t = Tester(State(
        relations=[Relation(
            endpoint='openfga',
            interface='openfga',
            remote_app_name='remote',
            remote_app_data={
                'store_name': 'test-store'
            }
        )]
    ))
    t.run('openfga-relation-changed')
    t.assert_schema_valid()

