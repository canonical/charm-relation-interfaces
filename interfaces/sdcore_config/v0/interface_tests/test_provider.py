# Copyright 2024 Canonical
# See LICENSE file for licensing details.

from interface_tester import Tester
from scenario import State, Relation
import json


def test_no_data_on_created():
    t = Tester()
    t.run("sdcore-config-relation-created")
    t.assert_relation_data_empty()


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
    t.run("sdcore-config-relation-created")
    t.assert_relation_data_empty()


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
    t.run("sdcore-config-relation-joined")
    t.assert_schema_valid()
