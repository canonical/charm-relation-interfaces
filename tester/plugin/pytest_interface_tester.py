import dataclasses
import logging
import operator
import tempfile
from pathlib import Path
from subprocess import PIPE, Popen
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    Literal,
    Optional,
    Tuple,
    Type,
    Union,
)

import pytest
from ops.testing import CharmType
from scenario.state import Event, Relation, State, _CharmSpec
from tester.plugin.interface_test import DataBagSchema, SchemaConfig

from collect_interface_tests import InterfaceTestSpec, gather_test_spec_for_version

if TYPE_CHECKING:
    from tester.plugin.interface_test import _InterfaceTestCase

Callback = Callable[[State, Event], None]

logger = logging.getLogger("pytest_interface_tester")
ROLE_TO_ROLE_META = {"provider": "provides", "requirer": "requires"}
Role = Literal["provider", "requirer"]


class InterfaceTesterValidationError(ValueError):
    """Raised if the InterfaceTester configuration is incorrect or incomplete."""


class InvalidTestCaseError(RuntimeError):
    """Raised if an interface test case is invalid."""


class InterfaceTester:
    def __init__(
        self,
        repo: str = "https://github.com/PietroPasotti/charm-relation-interfaces",
        branch: str = "main",
        base_path: str = "interfaces",
    ):
        self._repo = repo
        self._branch = branch
        self._base_path = base_path

        # set by .configure()
        self._charm_type = None
        self._meta = None
        self._actions = None
        self._config = None
        self._interface_name = None
        self._interface_version = 0
        self._state_template = None

        self._charm_spec_cache = None

    def configure(
        self,
        *,
        charm_type: Optional[Type[CharmType]] = None,
        repo: Optional[str] = None,
        branch: Optional[str] = None,
        base_path: Optional[str] = None,
        interface_name: Optional[str] = None,
        interface_version: Optional[int] = None,
        state_template: Optional[State] = None,
        meta: Optional[Dict[str, Any]] = None,
        actions: Optional[Dict[str, Any]] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """

        :arg interface_name: the interface to test.
        :param interface_version: what version of this interface we should be testing.
        :arg state_template: template state to use with the scenario test.
            The plugin will inject the relation spec under test, unless already defined.
        :param charm_type: The charm to test.
        :param repo: Repo to fetch the tests from.
        :param branch: Branch to fetch the tests from.
        :param base_path: path to an interfaces-compliant subtree within the repo.
        :param meta: charm metadata.yaml contents.
        :param actions: charm actions.yaml contents.
        :param config: charm config.yaml contents.
        """
        if charm_type:
            self._charm_type = charm_type
        if actions:
            self._actions = actions
        if meta:
            self._meta = meta
        if config:
            self._config = config
        if repo:
            self._repo = repo
        if interface_name:
            self._interface_name = interface_name
        if interface_version is not None:
            self._interface_version = interface_version
        if state_template:
            self._state_template = state_template
        if branch:
            self._branch = branch
        if base_path:
            self._base_path = base_path

    def _validate_config(self):
        """Validate the state of this object and raise InterfaceTesterValidationError if invalid."""
        errors = []
        if (self._actions or self._config) and not self._meta:
            errors.append(
                "Tester misconfigured: cannot set actions and config without setting meta."
            )
        if not self._charm_type:
            errors.append("Tester misconfigured: needs a charm_type set.")
        if not self.meta:
            errors.append(
                "no metadata: it was not provided, and it cannot be autoloaded"
            )
        if not self._repo:
            errors.append("repo missing")
        if not self._interface_name:
            errors.append("interface_name missing")
        if self._state_template and not isinstance(self._state_template, State):
            errors.append(
                f"state_template should be of type State, "
                f"not: {type(self._state_template)}"
            )
        if errors:
            err = "\n".join(errors)
            raise InterfaceTesterValidationError(
                f"pytest-interface-tester is misconfigured:\n{err}\n"
                f"please use the configure() API to provide the missing pieces."
            )

    @property
    def _charm_spec(self) -> _CharmSpec:
        """Return the _CharmSpec object representing the charm being tested and all its metadata."""
        if not self._charm_spec_cache:
            # We try to use Scenario's internal autoload functionality to autoload the charm spec.
            try:
                spec = _CharmSpec.autoload(self._charm_type)
                # if no metadata.yaml can be found in the charm type module's parent directory,
                # this call will raise:

            except FileNotFoundError as e:
                # if we have _meta set, we're good, otherwise we're misconfigured.
                if self._meta and self._charm_type:
                    spec = _CharmSpec(
                        meta=self._meta,
                        actions=self._actions,
                        config=self._config,
                        charm_type=self._charm_type,
                    )
                else:
                    raise InterfaceTesterValidationError(
                        "This InterfaceTester is missing charm metadata `meta` or a `charm type`. "
                        "Unable to load charm spec. Please provide both using the `configure` API."
                    ) from e
            self._charm_spec_cache = spec
        return self._charm_spec_cache

    @property
    def meta(self) -> dict:
        """Contents of the metadata.yaml of the charm being tested."""
        return self._meta or self._charm_spec.meta

    @property
    def actions(self) -> dict:
        """Contents of the actions.yaml of the charm being tested, if any."""
        return self._actions or self._charm_spec.actions

    @property
    def config(self) -> dict:
        """Contents of the config.yaml of the charm being tested, if any."""
        return self._config or self._charm_spec.config

    def _collect_interface_test_specs(self) -> InterfaceTestSpec:
        """Gathers the test cases as defined in the charm-relation-interfaces repo, for provider and requirer."""
        with tempfile.TemporaryDirectory() as tempdir:
            cmd = f"git clone --depth 1 --branch {self._branch} {self._repo}".split(" ")
            proc = Popen(cmd, cwd=tempdir, stderr=PIPE, stdout=PIPE)
            proc.wait()
            if proc.returncode != 0:
                raise RuntimeError(
                    f"failed to fetch {self._repo}:{self._branch}, "
                    f"check that the ref is correct. "
                    f"out={proc.stdout.read()}"
                    f"err={proc.stderr.read()}"
                )

            repo_name = self._repo.split("/")[-1]
            intf_spec_path = (
                Path(tempdir)
                / repo_name
                / self._base_path
                / self._interface_name.replace("-", "_")
                / f"v{self._interface_version}"
            )
            if not intf_spec_path.exists():
                raise RuntimeError(
                    f"interface spec dir not found at expected location. "
                    f"Check that {repo_name}/{self._base_path}/{self._interface_name} "
                    f"is a valid path in the remote repo you've selected as test case source "
                    f"for the plugin."
                )

            tests = gather_test_spec_for_version(
                intf_spec_path,
                interface_name=self._interface_name,
                version=self._interface_version,
            )

        return tests

    def _gather_supported_endpoints(self) -> Dict[Literal[Role], List[str]]:
        """Given a relation interface name, return a list of supported endpoints as either provider or requirer.

        These are collected from the charm's metadata.yaml.
        """
        supported_endpoints: Dict[Literal[Role], List[str]] = {}
        role: Role
        for role in ("provider", "requirer"):
            meta_role = ROLE_TO_ROLE_META[role]

            # assuming there's been a _validate_config() before this point, it's safe to access `meta`.
            endpoints = self.meta.get(meta_role, {})
            # if there are no endpoints using this interface, this means that this charm does not
            # support that role in the relation. There MIGHT still be tests for the other role, but they
            # are then meant for a charm implementing the other role.

            endpoints_for_interface = [
                k
                for k, v in endpoints.items()
                if v["interface"] == self._interface_name
            ]

            if endpoints_for_interface:
                supported_endpoints[role] = endpoints_for_interface
            else:
                logger.warning(f"skipping role {role}: unsupported by this charm.")

        return supported_endpoints

    def _yield_tests(
        self,
    ) -> Generator[
        Tuple["_InterfaceTestCase", "DataBagSchema", Event, State], None, None
    ]:
        """Yield all test cases applicable to this charm and interface.

        This means:
        - collecting the test cases (InterfaceTestCase objects) as defined by the charm-relation-interfaces
          specification. These tests encode what it means to satisfy this relation interface, and include some optional
          set-up logic for the State the test has to be run with.
        - obtaining the mocker/charm spec, as provided by the charm repo which hosts the source of the charm we
          are currently testing.
        - obtain from the charm's metadata.yaml the endpoints supporting this interface (in either role).
        - for each endpoint, for each applicable test case, yield: the test case, the schema as
          specified by the interface, the event and the State.
        """

        interface_name = self._interface_name
        tests = self._collect_interface_test_specs()

        if not (tests["provider"]["tests"] or tests["requirer"]["tests"]):
            yield from ()
            return

        supported_endpoints = self._gather_supported_endpoints()
        if not supported_endpoints:
            raise RuntimeError(
                f"this charm does not declare any endpoint using {interface_name}."
            )

        role: Role
        for role in supported_endpoints:
            logger.debug(f"collecting scenes for {role}")

            spec = tests[role]
            test: "_InterfaceTestCase"
            for test in spec["tests"]:
                logger.debug(f"converting {test} to ")

                # this is the input state as specified by the interface tests writer. It can contain elements
                # that are required for the relation interface test to work, typically relation data pertaining to the
                # relation interface being tested.
                input_state = test.input_state

                # state_template is state as specified by the charm being tested, which the charm requires to function
                # properly. Consider it part of the mocking. For example: some required config, a "happy" status,
                # network information, OTHER relations. Typically, should NOT touch the relation that this
                # interface test is about
                #  -> so we overwrite and warn on conflict: state_template is the baseline, input_state provides the
                #  relation spec for the relation being tested

                state = (self._state_template or State()).copy()

                relations = self._generate_relations_state(
                    state, input_state, supported_endpoints, role
                )
                state.relations = relations

                # the Relation instance this test is about:
                relation = next(
                    filter(lambda r: r.interface == self._interface_name, relations)
                )
                # test.EVENT might be a string or an Event. Cast to Event.
                evt = self._coerce_event(test.event, relation)

                logger.info(f"collected test for {interface_name} with {evt.name}")
                logger.debug(f"state={state}, evt={evt}")
                yield test, spec["schema"], evt, state

    def run(self):
        """Run interface tests."""
        self._validate_config()  # will raise if misconfigured

        errors = []
        ran_some = False

        for test, schema, event, state in self._yield_tests():
            out = self._run_test_case(test, schema, event, state)

            if out:
                errors.extend(out)
            ran_some = True

        if errors:
            pytest.fail(f"interface tests completed with errors. {errors}")

        if not ran_some:
            msg = f"no tests gathered for {self._interface_name}/v{self._interface_version}"
            logger.warning(msg)
            pytest.skip(msg)

    def _assert_case_plays(self, event: Event, state: State):
        try:
            state_out = state.trigger(
                event,
                charm_type=self._charm_type,
                meta=self.meta,
                actions=self.actions,
                config=self.config,
            )
        except Exception as e:
            msg = f"Failed check 1: scenario errored out: ({type(e).__name__}){e}. Could not play scene."
            raise RuntimeError(msg) from e
        return state_out

    @staticmethod
    def _assert_state_out_valid(state: State, test: "_InterfaceTestCase"):
        try:
            test.run(state)
        except Exception as e:
            msg = f"Failed check 2: validating scene output: {e}"
            raise RuntimeError(msg) from e

    @staticmethod
    def _assert_schema_valid(schema: DataBagSchema, relation: Relation) -> None:
        try:
            schema.validate(
                {
                    "unit": relation.local_unit_data,
                    "app": relation.local_app_data,
                }
            )
        except Exception as e:
            msg = f"Failed check 3: validating schema on scene output: {e}"
            logger.error(msg)
            raise RuntimeError(msg) from e

    def _assert_schemas_valid(
        self,
        test: "_InterfaceTestCase",
        state_out: State,
        schema: DataBagSchema,
    ) -> List[str]:
        """Check that all relations using the interface comply with the provided schema."""
        test_schema = test.schema
        if test_schema is SchemaConfig.skip:
            logger.info(
                "Schema validation skipped as per interface_test_case schema config."
            )
            return []

        if test_schema == SchemaConfig.default:
            schema = schema
        elif test_schema == SchemaConfig.empty:
            schema = DataBagSchema()
        elif isinstance(test_schema, DataBagSchema):
            schema = test_schema
        else:
            raise InvalidTestCaseError(
                "interface_test_case schema should be either a SchemaConfig instance or a "
                f"DataBagSchema instance, not {type(test_schema)}."
            )

        errors = []
        interface_name = self._interface_name
        for relation in [
            r for r in state_out.relations if r.interface == interface_name
        ]:
            try:
                self._assert_schema_valid(schema=schema, relation=relation)
            except RuntimeError as e:
                errors.append(e.args[0])
        return errors

    def _run_test_case(
        self,
        test: "_InterfaceTestCase",
        schema: Optional["DataBagSchema"],
        event: Event,
        state: State,
    ) -> List[str]:
        """Run an interface test case.

        This will run three checks in sequence:
        - play the scenario (check that the charm runs without exceptions) and
          obtain the output state
        - validate the output state (by calling the test-case-provided validator with
          the output state as argument)
        - validate the schema against the relations in the output state.

        It will return a list of strings, representing any issues encountered in any of the checks.
        """
        errors: List[str] = []

        logger.info("check 1: scenario play")
        try:
            state_out = self._assert_case_plays(event=event, state=state)
        except RuntimeError as e:
            errors.append(e.args[0])
            logger.info("scenario couldn't run: aborting test.")
            return errors

        logger.info("check 2: scenario output state validation")
        # todo: consistency check? or should we rely on scenario's?
        try:
            self._assert_state_out_valid(state_out, test)
        except RuntimeError as e:
            errors.append(e.args[0])

        logger.info("check 3: databag schema validation")
        if not schema:
            logger.info("schema validation step skipped: no schema provided")
            return errors
        errors.extend(self._assert_schemas_valid(test, state_out, schema))
        return errors

    def _coerce_event(self, raw_event: Union[str, Event], relation: Relation) -> Event:
        # if the event being tested is a relation event, we need to inject some metadata
        # or scenario.Runtime won't be able to guess what envvars need setting before ops.main
        # takes over
        if isinstance(raw_event, str):
            ep_name, _, evt_kind = raw_event.rpartition("-relation-")
            if ep_name and evt_kind:
                # this is a relation event.
                # we inject the relation metadata
                # todo: if the user passes a relation event that is NOT about the relation interface that this test is
                #  about, at this point we are injecting the wrong Relation instance.
                #  e.g. if in interfaces/foo one wants to test that if 'bar-relation-joined' is fired...
                #  then one would have to pass an Event instance already with its own Relation.
                return Event(
                    raw_event,
                    relation=relation.replace(endpoint=ep_name),
                )

            else:
                return Event(raw_event)

        elif isinstance(raw_event, Event):
            if raw_event._is_relation_event and not raw_event.relation:
                raise InvalidTestCaseError(
                    "This test case was passed an Event representing a relation event."
                    "However it does not have a Relation. Please pass it to the Event like so: "
                    "evt = Event('my_relation_changed', relation=Relation(...))"
                )

            return raw_event

        else:
            raise InvalidTestCaseError(
                f"Expected Event or str, not {type(raw_event)}. "
                f"Invalid test case: {self} cannot cast {raw_event} to Event."
            )

    def _generate_relations_state(
        self, state_template: State, input_state: State, supported_endpoints, role: Role
    ) -> List[Relation]:
        """Merge the relations from the input state and the state template into one.

        The charm being tested possibly provided a state_template to define some setup mocking data.
        The interface tests also have an input_state. Here we merge them into one relation list to be passed to
        the 'final' State the test will run with.
        """
        interface_name = self._interface_name

        for rel in state_template.relations:
            if rel.interface == interface_name:
                logger.warning(
                    f"relation with interface name = {interface_name} found in state template. "
                    f"This will be overwritten by the relation spec provided by the relation "
                    f"interface test case."
                )

        def filter_relations(rels: List[Relation], op: Callable):
            return [r for r in rels if op(r.interface, interface_name)]

        # the baseline is: all relations whose interface IS NOT the interface we're testing.
        relations = filter_relations(state_template.relations, op=operator.ne)

        if input_state:
            # if the charm we're testing specified some relations in its input state, we add those whose interface IS
            # the same as the one we're testing. If other relation interfaces were specified, they will be ignored.
            relations.extend(filter_relations(input_state.relations, op=operator.eq))

            if ignored := filter_relations(input_state.relations, op=operator.eq):
                logger.warning(
                    f"irrelevant relations specified in input state for {interface_name}/{role}."
                    f"These will be ignored. details: {ignored}"
                )

        # if we still don't have any relation matching the interface we're testing, we generate one from scratch.
        if not filter_relations(relations, op=operator.eq):
            # if neither the charm nor the interface specified any custom relation spec for
            # the interface we're testing, we will provide one.
            endpoints_for_interface = supported_endpoints[role]

            if len(endpoints_for_interface) < 1:
                raise ValueError(f"no endpoint found for {role}/{interface_name}.")
            elif len(endpoints_for_interface) > 1:
                raise ValueError(
                    f"Multiple endpoints found for {role}/{interface_name}: "
                    f"{endpoints_for_interface}: cannot guess which one it is "
                    f"we're supposed to be testing"
                )
            else:
                endpoint = endpoints_for_interface[0]

            relations.append(
                Relation(
                    interface=interface_name,
                    endpoint=endpoint,
                )
            )
        logger.debug(
            f"{self}: merged {input_state} and {state_template} --> relations={relations}"
        )
        return relations


@pytest.fixture(scope="function")
def interface_tester():
    yield InterfaceTester()
