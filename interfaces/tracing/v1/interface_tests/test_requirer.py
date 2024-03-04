# Copyright 2024 Canonical
# See LICENSE file for licensing details.

from interface_tester.interface_test import Tester


# on created, joined, changed: the requirer is expected to publish a list of requested receivers
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
