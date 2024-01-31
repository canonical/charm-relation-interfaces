# Copyright 2023 Canonical
# See LICENSE file for licensing details.
import json

from interface_tester.interface_test import Tester
from scenario import State, Relation


# no matter what's in the remote databags, the tracing v1 provider will always populate with valid data.

def test_data_on_created():
    tester = Tester()
    tester.run('tracing-relation-created')
    tester.assert_schema_valid()


def test_data_on_joined():
    tester = Tester()
    tester.run('tracing-relation-joined')
    tester.assert_schema_valid()


def test_data_on_changed():
    tester = Tester()
    tester.run('tracing-relation-changed')
    tester.assert_schema_valid()


# even if the remote side sends rubbish
def test_data_on_changed_bad_remote_data():
    tester = Tester(
        state_in=State(
            relations=[Relation(
                endpoint='tracing',
                interface='tracing',
                remote_app_name='remote',
                remote_app_data={
                    "bubble": "rubble"
                }
            )]
        )
    )
    tester.run('tracing-relation-changed')
    tester.assert_schema_valid()
