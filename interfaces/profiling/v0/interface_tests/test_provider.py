# Copyright 2024 Canonical
# See LICENSE file for licensing details.
import json

from interface_tester.interface_test import Tester

# on created, joined, changed: the provider is expected to publish all data
def test_data_on_created():
    tester = Tester()
    tester.run('profiling-relation-created')
    tester.assert_schema_valid()


def test_data_on_joined():
    tester = Tester()
    tester.run('profiling-relation-joined')
    tester.assert_schema_valid()


def test_data_on_changed():
    tester = Tester()
    tester.run('profiling-relation-changed')
    tester.assert_schema_valid()
