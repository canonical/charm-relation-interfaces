# Copyright 2024 Canonical
# See LICENSE file for licensing details.

from interface_tester import Tester


def test_no_data_on_created():
    # Nothing happens on created: databags are empty
    t = Tester()
    state_out = t.run("prometheus-scrape-relation-created")
    t.assert_relation_data_empty()


def test_no_data_on_joined():
    # Nothing happens on joined: databags are empty
    t = Tester()
    state_out = t.run("prometheus-scrape-relation-joined")
    t.assert_schema_valid()
