import logging
import operator
import tempfile
from pathlib import Path
from subprocess import Popen, PIPE
from typing import Union, Optional, Type, Iterable, Callable, TYPE_CHECKING, Literal, Tuple, Dict, Any

import pytest
from ops.testing import CharmType
from scenario.scenario import Scenario
from scenario.structs import State, CharmSpec, Scene, event, Event, EventMeta, RelationMeta, relation

from collect_interface_tests import gather_test_spec_for_version, InterfaceTestSpec

if TYPE_CHECKING:
    from tester.plugin.interface_test import InterfaceTestCase, DataBagSchema

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
        self._interface_name = None
        self._state_template = None

    def configure(self, *,
                  target: Union[Type[CharmType], CharmSpec] = None,
                  repo: Optional[str] = None,
                  branch: Optional[str] = None,
                  base_path: Optional[str] = None,
                  interface_name: str = None,
                  state_template: Optional[State] = None
                  ):
        """

        :arg interface_name: the interface to test.
        :arg state_template: template state to use with the scenario test.
            The plugin will inject the relation spec under test, unless already defined.
        :param target: The charm or charmspec to test.
        :param repo: Repo to fetch the tests from.
        :param branch: Branch to fetch the tests from.
        :param base_path: path to an interfaces-compliant subtree within the repo.
        :return:
        """
        if target:
            self._target = target
        if repo:
            self._repo = repo
        if interface_name:
            self._interface_name = interface_name
        if state_template:
            self._state_template = state_template
        if branch:
            self._branch = branch
        if base_path:
            self._base_path = base_path

    def _check_config(self):
        errors = []
        if not self._target:
            errors.append('target missing')
        if not self._repo:
            errors.append('repo missing')
        if not self._interface_name:
            errors.append('interface_name missing')
        if self._state_template and not isinstance(self._state_template, State):
            errors.append(f'state_template should be of type State, '
                          f'not: {type(self._state_template)}')
        if errors:
            err = '\n'.join(errors)
            raise ValueError('pytest-interface-tester is misconfigured:'
                             f'{err}')

    @property
    def _spec(self) -> CharmSpec:
        if isinstance(self._target, CharmSpec):
            return self._target
        spec = CharmSpec.from_charm(self._target)
        if not spec.meta:
            raise RuntimeError(f'cannot autoload charm spec from target = {self._target}:'
                               f'failed to find metadata file. Please pass a full CharmSpec instead.')
        return spec

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
            intf_spec_path = Path(tempdir) / repo_name / self._base_path / interface_name.replace('-', '_') / f"v{version}"
            if not intf_spec_path.exists():
                raise RuntimeError(f"interface spec dir not found at expected location. "
                                   f"Check that {repo_name}/{self._base_path}/{interface_name} "
                                   f"is a valid path in the remote repo you've selected as test case source "
                                   f"for the plugin.")

            tests = gather_test_spec_for_version(intf_spec_path)
        return tests

    def _yield_tests(self,
                      interface_name: Optional[str] = None,
                      state_template: Optional[State] = None,
                      version: int = 0
                      ) -> Iterable[Tuple["InterfaceTestCase", "DataBagSchema", Scene]]:

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
            spec = tests[role]
            for _, test in spec['tests']:
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
                    return [r for r in relations if op(r.meta.interface, interface_name)]

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

                schema = spec['schema']
                yield test, schema, scene

    def run(self, subtests=None):
        """Run interface tests."""
        self._check_config()  # will raise if misconfigured

        interface_name = self._interface_name

        errors = []

        for test, schema, scene in self._yield_tests(
                interface_name,
                state_template=self._state_template):
            if subtests:
                with subtests.test(msg=getattr(test, 'name', test.__name__)):
                    self._run(test, schema, scene, _raise=True)

            out = self._run(test, schema, scene)
            if out:
                errors.extend(out)

        if errors:
            pytest.fail(f'interface tests completed with errors. {errors}')


    def _run(self, test: "InterfaceTestCase", schema:Optional["DataBagSchema"], scene:Scene,
             _raise=False):
        errors = []
        scenario = Scenario(charm_spec=self._spec)

        logger.info('check 1: scenario play')
        try:
            out = scenario.play(scene)
        except Exception as e:
            msg = f"Failed check 1: scenario errored out: ({type(e).__name__}){e}. Could not play scene."
            logger.error(msg)
            if _raise:
                raise RuntimeError(msg) from e
            errors.append(msg)
            # if this one fails, it doesn't make sense to try the next.
            return errors

        logger.info('check 2: scenario output state validation')
        # todo: out consistency check ? or we rely on scenario's.
        try:
            # todo consider validate(output: RelationSpec) and INPUT_STATE: RelationSpec to simplify.
            test.validate(out)
        except Exception as e:
            msg = f"Failed check 2: validating scene output: {e}"
            logger.error(msg)
            if _raise:
                raise RuntimeError(msg) from e

            errors.append(msg)
            return errors

        logger.info('check 3: databag schema validation')
        if not schema:
            logger.info('schema validation step skipped: no schema provided')
            return errors

        interface_name = self._interface_name
        for rel in [r for r in out.relations if r.meta.interface == interface_name]:
            try:
                app_valid, unit_valid = test.validate_schema(rel, schema=schema)
            except Exception as e:
                msg = f"Failed check 3: validating schema on scene output: {e}"
                logger.error(msg)
                if _raise:
                    raise RuntimeError(msg) from e

                errors.append(msg)
                continue
            logger.info(f"schema validation: app={app_valid}, unit={unit_valid}")
        return errors

@pytest.fixture(scope='function')
def interface_tester():
    yield InterfaceTester()
