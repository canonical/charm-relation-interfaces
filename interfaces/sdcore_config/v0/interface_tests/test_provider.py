# Copyright 2024 Canonical
# See LICENSE file for licensing details.

from interface_tester.interface_test import Tester
from scenario import State, Relation


def test_data_published_on_created():
    t = Tester(
        State(
            relations=[
                Relation(
                    endpoint="sdcore_config",
                    interface="sdcore_config",
                )
            ],
        )
    )
    state_out: State = t.run("sdcore-config-relation-created")
    t.assert_schema_valid()
    assert state_out.unit_status.name == 'active'


def test_data_published_on_joined():
    t = Tester(
        State(
            relations=[
                Relation(
                    endpoint="sdcore_config",
                    interface="sdcore_config",
                )
            ],
        )
    )
    state_out: State = t.run("sdcore-config-relation-joined")
    t.assert_schema_valid()
    assert state_out.unit_status.name == 'active'


def test_data_published_on_changed():
    t = Tester(
        State(
            relations=[
                Relation(
                    endpoint="sdcore_config",
                    interface="sdcore_config",
                )
            ],
        )
    )
    state_out: State = t.run("sdcore-config-relation-changed")
    t.assert_schema_valid()
    assert state_out.unit_status.name == 'active'


def test_no_data_on_broken():
    t = Tester(
        State(
            relations=[
                Relation(
                    endpoint="sdcore_config",
                    interface="sdcore_config",
                )
            ],
        )
    )
    state_out: State = t.run("sdcore-config-relation-broken")
    t.assert_relation_data_empty()
    assert state_out.unit_status.name == 'active'

