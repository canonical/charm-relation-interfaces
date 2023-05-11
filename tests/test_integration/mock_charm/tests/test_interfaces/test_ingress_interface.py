# Copyright 2023 Canonical
# See LICENSE file for licensing details.
from unittest.mock import patch

import pytest
from interface_tester import InterfaceTester
from interface_tester.errors import InterfaceTestsFailed, NoTestsRun


def test_ingress_interface(interface_tester: InterfaceTester):
    interface_tester.configure(interface_name="ingress", interface_version=1)
    interface_tester.run()


def test_ingress_interface_fails(interface_tester: InterfaceTester):
    # if we disable using the ingress lib, this test would fail schema validation.
    with patch("charm.MyCharm.use_ingress", False):
        interface_tester.configure(interface_name="ingress", interface_version=1)
        with pytest.raises(InterfaceTestsFailed):
            interface_tester.run()


def test_notests_interface_fails(interface_tester: InterfaceTester):
    interface_tester.configure(
        # nonexistent interface
        interface_name="foobarbaz",
        interface_version=0,
    )
    with pytest.raises(NoTestsRun):
        interface_tester.run()
