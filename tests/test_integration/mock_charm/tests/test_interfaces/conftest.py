from unittest.mock import patch

import pytest
from charm import MyCharm
from interface_tester import InterfaceTester
from ops.pebble import Layer
from scenario.state import Container, State


@pytest.fixture
def interface_tester(interface_tester: InterfaceTester):
    with patch("charm.KubernetesServicePatch", lambda **unused: None):
        interface_tester.configure(
            repo="https://github.com/canonical/charm-relation-interfaces",
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
