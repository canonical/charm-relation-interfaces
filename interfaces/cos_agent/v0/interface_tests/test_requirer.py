# Copyright 2024 Canonical
# See LICENSE file for licensing details.

from interface_tester import Tester

def test_no_data_on_created():
    # nothing happens on created: databags are empty
    t = Tester()
    state_out = t.run("cos-agent-created")
    t.assert_relation_data_empty()
