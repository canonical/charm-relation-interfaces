from pathlib import Path

import yaml
from ops.charm import CharmBase
from ops.framework import Framework
from ops.model import BlockedStatus
from scenario import State

from collect_interface_tests import InterfaceTestSpec, gather_test_spec_for_version
from pytest_interface_tester import InterfaceTester

PROJECT_ROOT = Path(__file__).parent.parent.parent


class MyProvider(CharmBase):
    META = {"name": "local", "provides": {"ingress": {"interface": "ingress"}}}

    def __init__(self, framework: Framework):
        super().__init__(framework)
        self.framework.observe(self.on.ingress_relation_changed, self._on_changed)

    def _on_changed(self, e):
        if e.relation.data[e.relation.app].get("host"):
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
            e.relation.data[self.app]["host"] = "foo"
            e.relation.data[self.app]["port"] = "10"
            e.relation.data[self.app]["model"] = "baz"
            e.relation.data[self.app]["name"] = self.unit.name


class TestingInterfaceTester(InterfaceTester):
    def _collect_interface_test_specs(self) -> InterfaceTestSpec:
        return gather_test_spec_for_version(
            PROJECT_ROOT
            / "interfaces"
            / self._interface_name
            / f"v{self._interface_version}",
            self._interface_name,
            self._interface_version,
        )


def test_ingress_requirer(subtests):
    tester = TestingInterfaceTester()
    tester.configure(
        charm_type=MyRequirer,
        meta=MyRequirer.META,
        interface_name="ingress",
        state_template=State(leader=True),
    )
    assert list(tester._yield_tests()), "no tests ran"
    tester.run(subtests=subtests)


def test_ingress_provider(subtests):
    tester = TestingInterfaceTester()
    tester.configure(
        charm_type=MyProvider,
        meta=MyProvider.META,
        interface_name="ingress",
        state_template=State(leader=True),
    )
    assert list(tester._yield_tests()), "no tests ran"
    tester.run(subtests=subtests)
