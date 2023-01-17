from typing import Union, Optional, Type, Iterable, Callable

import pytest
from ops.testing import CharmType
from scenario.scenario import Scenario
from scenario.structs import State, CharmSpec, Scene

Callback = Callable[[Scene], None]


class InterfaceTester:
    def __init__(self):
        self._target = None

    def configure(self, *, target: Union[Type[CharmType], CharmSpec]):
        self._target = target

    @property
    def _spec(self) -> CharmSpec:
        if isinstance(self._target, CharmSpec):
            return self._target
        return CharmSpec.from_charm(self._target)

    def _yield_scenes(self,
                          interface_name: Optional[str] = None,
                          state_template: Optional[State] = None
                          ) -> Iterable[Union[Scene, Callback]]:

        if interface_name:
            # TODO: implement
            pass

    def run(self,
            interface_name: Optional[str] = None,
            state_template: Optional[State] = None
            ):
        """Run interface tests on this charm.

        :arg interface_name: the interface to test.
        :arg state_template: template state to use with the scenario test. The plugin will inject the relation spec under test,
            unless already defined.
        """

        scenario = Scenario(charm_spec=self._spec)

        for scene in self._yield_scenes(
                interface_name,
                state_template=state_template):

            try:
                # if this raises: the test fails.
                out = scenario.play(scene)
            except Exception:
                pytest.fail("scenario errored out")

            # todo: out consistency check ?


@pytest.fixture(scope='function')
def interface_tester():
    yield InterfaceTester()
