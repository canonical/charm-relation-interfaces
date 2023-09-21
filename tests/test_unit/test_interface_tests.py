import json
from pathlib import Path

import pytest
import yaml
from interface_tester.collector import InterfaceTestSpec, gather_test_spec_for_version
from interface_tester.errors import NoTestsRun
from interface_tester.plugin import InterfaceTester
from ops.charm import CharmBase
from ops.framework import Framework
from ops.model import BlockedStatus
from scenario import State

PROJECT_ROOT = Path(__file__).parent.parent.parent


class MyProvider(CharmBase):
    META = {"name": "local", "provides": {"ingress": {"interface": "ingress"}}}

    def __init__(self, framework: Framework):
        super().__init__(framework)
        self.framework.observe(self.on.ingress_relation_changed, self._on_changed)

    def _on_changed(self, e):
        appdata = e.relation.data[e.relation.app]
        # simplification of valid ingress requirer data
        if all(appdata.get(key) for key in ("host", "port", "model", "name")):
            url = yaml.safe_dump({"url": "http://foo.com"})
            e.relation.data[self.app]["ingress"] = url
        else:
            self.unit.status = BlockedStatus("relation data invalid")


class MyRequirer(CharmBase):
    META = {"name": "local", "requires": {"ingress": {"interface": "ingress"}}}

    def __init__(self, framework: Framework):
        super().__init__(framework)
        self.framework.observe(self.on.ingress_relation_created, self._on_created)

    def _on_created(self, e):
        if self.unit.is_leader():
            data = {
                "host": '"foo"',
                "port": "10",
                "model": '"baz"',
                "name": json.dumps(self.unit.name),
            }
            e.relation.data[self.app]["data"] = yaml.safe_dump(data)


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


def test_ingress_requirer():
    tester = _MockInterfaceTester()
    tester.configure(
        charm_type=MyRequirer,
        meta=MyRequirer.META,
        interface_name="ingress",
        interface_version=1,
        state_template=State(leader=True),
    )

    # ATM there are no interface tests for ingress v1 requirer
    with pytest.raises(NoTestsRun):
        tester.run()


def test_ingress_provider():
    tester = _MockInterfaceTester()
    tester.configure(
        charm_type=MyProvider,
        meta=MyProvider.META,
        interface_name="ingress",
        interface_version=1,
        state_template=State(leader=True),
    )
    tester.run()
