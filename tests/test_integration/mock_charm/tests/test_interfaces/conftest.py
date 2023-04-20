from pathlib import Path
from unittest.mock import patch

import pytest
from charm import MyCharm
from interface_tester import InterfaceTester
from interface_tester.collector import InterfaceTestSpec, gather_test_spec_for_version
from ops.pebble import Layer
from scenario.state import Container, State

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent.parent


class _MockInterfaceTester(InterfaceTester):
    # Instead of cloning the charm-relation-interfaces repo, use the local one we're in.
    def _collect_interface_test_specs(self) -> InterfaceTestSpec:
        return gather_test_spec_for_version(
            PROJECT_ROOT
            / "interfaces"
            / self._interface_name
            / f"v{self._interface_version}",
            self._interface_name,
            self._interface_version,
        )


@pytest.fixture
def interface_tester():
    interface_tester = _MockInterfaceTester()
    with patch("charm.KubernetesServicePatch", lambda **unused: None):
        interface_tester.configure(
            charm_type=MyCharm,
            state_template=State(
                leader=True,
                config={
                    "external_hostname": "0.0.0.0",
                },
                containers=[
                    # unless the traefik service reports active,
                    # the charm won't publish the ingress url.
                    Container(
                        name="foo",
                        can_connect=True,
                        layers={
                            "foo": Layer(
                                {
                                    "summary": "foo",
                                    "description": "bar",
                                    "services": {
                                        "bar": {
                                            "startup": "enabled",
                                            "current": "active",
                                            "name": "bar",
                                        }
                                    },
                                    "checks": {},
                                }
                            )
                        },
                    )
                ],
            ),
        )
        yield interface_tester
