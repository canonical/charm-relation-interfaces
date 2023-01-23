import logging
import operator
import tempfile
from pathlib import Path
from subprocess import Popen, PIPE
from typing import Union, Optional, Type, Iterable, Callable, TYPE_CHECKING, Literal, Tuple

import pytest
from ops.testing import CharmType
from scenario.scenario import Scenario
from scenario.structs import State, CharmSpec, Scene, event, Event, EventMeta, RelationMeta, relation

from collect_interface_tests import gather_tests_for_version, InterfaceTestSpec

if TYPE_CHECKING:
    from tester.plugin.interface_test import InterfaceTestCase

Callback = Callable[[Scene], None]

logger = logging.getLogger('pytest_interface_tester')
ROLE_TO_ROLE_META = {'provider': 'provides', 'requirer': 'requires'}


class InterfaceTester:
    def __init__(self,
                 repo: str = "https://github.com/PietroPasotti/charm-relation-interfaces",
                 branch: str = "main",
                 base_path: str = "interfaces",
                 ):
        self._repo = repo
        self._branch = branch
        self._base_path = base_path
        self._target = None

    def configure(self, *,
                  target: Union[Type[CharmType], CharmSpec],
                  repo: Optional[str] = None,
                  branch: Optional[str] = None,
                  base_path: Optional[str] = None
                  ):
        self._target = target

        if repo:
            self._repo = repo
        if branch:
            self._branch = branch
        if base_path:
            self._base_path = base_path

    @property
    def _spec(self) -> CharmSpec:
        if isinstance(self._target, CharmSpec):
            return self._target
        return CharmSpec.from_charm(self._target)

    def _fetch_tests(self, interface_name, version: int = 0) -> InterfaceTestSpec:
        with tempfile.TemporaryDirectory() as tempdir:
            cmd = f"git clone --depth 1 --branch {self._branch} {self._repo}".split(" ")
            proc = Popen(cmd, cwd=tempdir, stderr=PIPE, stdout=PIPE)
            proc.wait()
            if proc.returncode != 0:
                raise RuntimeError(f'failed to fetch {self._repo}:{self._branch}, '
                                   f'check that the ref is correct. '
                                   f'out={proc.stdout.read()}'
                                   f'err={proc.stderr.read()}')

            repo_name = self._repo.split('/')[-1]
            intf_spec_path = Path(tempdir) / repo_name / self._base_path / interface_name / f"v{version}"
            if not intf_spec_path.exists():
                raise RuntimeError(f"interface spec dir not found at expected location. "
                                   f"Check that {repo_name}/ {self._base_path} /{interface_name} "
                                   f"is a valid path in the remote repo you've selected as test case source "
                                   f"for the plugin.")

            tests = gather_tests_for_version(intf_spec_path)
        return tests

    def _yield_scenes(self,
                      interface_name: Optional[str] = None,
                      state_template: Optional[State] = None,
                      version: int = 0
                      ) -> Iterable[Tuple["InterfaceTestCase", Scene]]:

        # in order to gather the scenes/test cases, we need two things:
        # - the test cases (InterfaceTestCase subclasses) as defined by the charm-relation interfaces repo
        # - the mocker/charm spec, as provided by the charm repo (the repo from which this code is
        #   being run, presumably).

        tests = self._fetch_tests(interface_name, version)

        if not (tests['provider']['tests'] or tests['requirer']['tests']):
            msg = f'no tests gathered for {interface_name}/v{version}'
            logger.warning(msg)
            pytest.skip(msg)

        supported_endpoints = {}
        for role in ('provider', 'requirer'):
            meta_role = ROLE_TO_ROLE_META[role]
            endpoints = self._spec.meta.get(meta_role, {})
            # if there are no endpoints using this interface, this means that this charm does not
            # support that role in the relation. There MIGHT still be tests for the other role, but they
            # are then meant for a charm implementing the other role.

            endpoints_for_interface = [k for k, v in endpoints.items() if v['interface'] == interface_name]

            if endpoints_for_interface:
                supported_endpoints[role] = endpoints_for_interface
            else:
                logger.warning(f'skipping role {role}: unsupported by this charm.')

        if not supported_endpoints:
            raise RuntimeError(f'this charm does not declare any endpoint using {interface_name}.')

        role: Literal['provider', 'requirer']
        for role in supported_endpoints:
            logger.debug(f'collecting scenes for {role}')

            test: "InterfaceTestCase"
            for _, test in tests[role]['tests']:
                logger.debug(f'converting {test} to Scene')

                # this is the input state as specified by the interface tests writer. It can contain elements
                # that are required for the relation interface test to work, typically relation data pertaining to the
                # relation interface being tested.
                input_state = test.INPUT_STATE

                # state_template is state as specified by the charm being tested, which the charm requires to function
                # properly. Consider it part of the mocking. For example: some required config, a "happy" status,
                # network information, OTHER relations. Typically, should NOT touch the relation that this
                # interface test is about
                #  -> so we overwrite and warn on conflict: state_template is the baseline, input_state provides the
                #  relation spec for the relation being tested

                state = (state_template or State()).copy()
                for rel in state.relations:
                    if rel.meta.interface == interface_name:
                        logger.warning(f"relation with interface name = {interface_name} found in state template. "
                                       f"This will be overwritten by the relation spec provided by the relation "
                                       f"interface test case.")

                def filter_relations(relations, op):
                    return [r for r in relations if op(rel.meta.interface, interface_name)]

                relations = filter_relations(state.relations, op=operator.ne)

                if input_state:
                    relations.extend(filter_relations(input_state.relations, op=operator.eq))

                if not filter_relations(relations, op=operator.eq):
                    # if neither the charm nor the interface specified any custom relation spec for
                    # the interface we're testing, we will provide one.
                    endpoints_for_interface = supported_endpoints[role]

                    if len(endpoints_for_interface) < 1:
                        raise ValueError(f'no endpoint found for {role}/{interface_name}.')
                    elif len(endpoints_for_interface) > 1:
                        raise ValueError(f"Multiple endpoints found for {role}/{interface_name}: "
                                         f"{endpoints_for_interface}: cannot guess which one it is "
                                         f"we're supposed to be testing")
                    else:
                        endpoint = endpoints_for_interface[0]

                    relations.append(
                        relation(
                            interface=interface_name,
                            endpoint=endpoint,
                        )
                    )

                state.relations = relations

                # if the event being tested is a relation event, we need to inject some metadata
                # or scenario.Runtime won't be able to guess what envvars need setting before ops.main
                # takes over
                if isinstance(test.EVENT, str):
                    ep_name, _, evt_kind = test.EVENT.rpartition('-relation-')
                    if ep_name and evt_kind:
                        # this is a relation event.
                        # we craft some metadata
                        evt = event(test.EVENT,
                                    meta=EventMeta(
                                        relation=RelationMeta(
                                            endpoint=ep_name,
                                            interface=interface_name,
                                            relation_id=0,
                                            remote_app_name='remote',
                                        )))

                    else:
                        evt = event(test.EVENT)

                elif isinstance(test.EVENT, Event):
                    evt = test.EVENT

                else:
                    raise TypeError(f"Expected Event or str, not {type(test.EVENT)}. "
                                    f"Invalid test case.")

                scene = Scene(
                    event=evt,
                    state=state
                )

                logger.info(f"collected {scene} for {interface_name}")

                yield test, scene

    def run(self,
            interface_name: Optional[str] = None,
            state_template: Optional[State] = None
            ):
        """Run interface tests on this charm.

        :arg interface_name: the interface to test.
        :arg state_template: template state to use with the scenario test.
            The plugin will inject the relation spec under test, unless already defined.
        """

        scenario = Scenario(charm_spec=self._spec)

        for test, scene in self._yield_scenes(
                interface_name,
                state_template=state_template):

            try:
                out = scenario.play(scene)
            except Exception as e:
                pytest.fail(f"scenario errored out: {e}. Could not play scene.")

            # todo: out consistency check ? or we rely on scenario's.

            try:
                test.validate(output_state=out)
            except Exception as e:
                pytest.fail(f"Failed validating scene output: {e}")

            try:
                test.validate_schema(output_state=out)
            except Exception as e:
                pytest.fail(f"Failed validating schema on scene output: {e}")





@pytest.fixture(scope='function')
def interface_tester():
    yield InterfaceTester()
