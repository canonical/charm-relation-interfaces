# Copyright 2023 Canonical
# See LICENSE file for licensing details.
import json

from interface_tester.interface_test import Tester
from scenario import State, Relation


def test_no_data_on_created():
    tester = Tester()
    tester.run('tracing-relation-created')
    tester.assert_relation_data_empty()


def test_no_data_on_joined():
    tester = Tester()
    tester.run('tracing-relation-joined')
    tester.assert_relation_data_empty()


def test_data_on_changed():
    tester = Tester(
        state_in=State(
            relations=[Relation(
                endpoint='tracing',
                interface='tracing',
                remote_app_name='remote',
                local_app_data={
                    "host": "foo.com",
                    "ingesters": json.dumps([
                        {"protocol": "otlp_grpc",
                         "port": "4242"}
                    ])
                }
            )]
        )
    )
    tester.run('tracing-relation-changed')
    tester.assert_schema_valid()
