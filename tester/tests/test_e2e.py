import json
from pathlib import Path
from typing import Optional

from ops.charm import CharmBase
from ops.framework import Framework
from ops.model import BlockedStatus
from scenario.structs import CharmSpec, State

from collect_interface_tests import gather_test_spec_for_version, InterfaceTestSpec
from pytest_interface_tester import InterfaceTester

PROJECT_ROOT = Path(__file__).parent.parent.parent


class MyProvider(CharmBase):
    META = {
        'name': 'local',
        'provides': {'ingress': {'interface': 'ingress'}}}

    def __init__(self, framework: Framework, key: Optional[str] = None):
        super().__init__(framework, key)
        self.framework.observe(self.on.ingress_relation_changed, self._on_changed)

    def _on_changed(self, e):
        if e.relation.data[e.relation.app].get('host'):
            urls = json.dumps({e.relation.data[e.relation.app].get('name'): {'url': 'http://foo.com'}})
            e.relation.data[self.app]['urls'] = urls
        else:
            self.unit.status = BlockedStatus('relation data invalid')


class MyRequirer(CharmBase):
    META = {
        'name': 'local',
        'requires': {'ingress': {'interface': 'ingress'}}}

    def __init__(self, framework: Framework, key: Optional[str] = None):
        super().__init__(framework, key)
        self.framework.observe(self.on.ingress_relation_created, self._on_created)

    def _on_created(self, e):
        if self.unit.is_leader():
            e.relation.data[self.app]['host'] = 'foo'
            e.relation.data[self.app]['port'] = '10'
            e.relation.data[self.app]['model'] = 'baz'
            e.relation.data[self.app]['name'] = self.unit.name


class TestingInterfaceTester(InterfaceTester):
    def _fetch_tests(self, interface_name, version: int = 0) -> InterfaceTestSpec:
        return gather_test_spec_for_version(PROJECT_ROOT / 'interfaces' / interface_name / f'v{version}')


def test_ingress_requirer(subtests):
    tester = TestingInterfaceTester()
    tester.configure(
        target=CharmSpec(
            charm_type=MyRequirer,
            meta=MyRequirer.META
        ),
        interface_name='ingress',
        state_template=State(
            leader=True
        )
    )
    tester.run(subtests=subtests)


def test_ingress_provider(subtests):
    tester = TestingInterfaceTester()
    tester.configure(
        target=CharmSpec(
            charm_type=MyProvider,
            meta=MyProvider.META
        ),
        interface_name='ingress',
        state_template=State(
            leader=True
        )
    )
    tester.run(subtests=subtests)
