# Copyright 2023 Canonical
# See LICENSE file for licensing details.
from unittest.mock import patch

import pytest
from interface_tester import InterfaceTester


def test_ingress_interface(interface_tester: InterfaceTester):
    interface_tester.configure(
        interface_name="ingress",
    )
    interface_tester.run()


@pytest.mark.xfail  # replace with pytest.raises after itester.run() raises a proper runtimeerror.
def test_ingress_interface_fails(interface_tester: InterfaceTester):
    # if we disable using the ingress lib, this test would fail schema validation.
    with patch("charm.MyCharm.use_ingress", False):
        interface_tester.configure(
            interface_name="ingress",
        )
        interface_tester.run()
