import dataclasses
import inspect
import logging
import re
import typing
from collections import defaultdict
from enum import Enum
from typing import Callable, Dict, List, Literal, Optional, Tuple, Union, Type

from ops.charm import CharmBase

from interfaces.schema_base import DataBagSchema
from scenario import Event, Relation, State

from errors import InvalidTestCaseError

if typing.TYPE_CHECKING:
    InterfaceNameStr = str
    VersionInt = int
    RoleLiteral = Literal["requirer", "provider"]
    _SchemaConfigLiteral = Literal["default", "skip", "empty"]

INTF_NAME_AND_VERSION_REGEX = re.compile(r"/interfaces/(\w+)/v(\d+)/")

logger = logging.getLogger(__name__)


class InvalidTestCase(RuntimeError):
    """Raised if a function decorated with interface_test_case is invalid."""


class SchemaConfig(str, Enum):
    """Class used to program the schema validator run that is paired with each test case."""

    default = "default"
    """Use this value if you want the test case to validate the output state's databags with the default schema."""
    skip = "skip"
    """Use this value if you want the test case skip schema validation altogether."""
    empty = "empty"
    """Use this value if you want the databag validator to assert that the databags are empty."""


class Role(str, Enum):
    provider = "provider"
    requirer = "requirer"


@dataclasses.dataclass
class _InterfaceTestCase:
    """Data associated with a single interface test case."""
    interface_name: str
    """The name of the interface that this test is about."""
    version: int
    """The version of the interface that this test is about."""
    event: Union[Event, str]
    """The event that this test is about."""
    role: Role
    """The role (provider|requirer) that this test is about."""
    name: str
    """Human-readable name of what this test does."""

    validator: Callable[[State], None]
    """The function that will be called on the output state to validate it."""

    schema: Union[DataBagSchema, SchemaConfig] = SchemaConfig.default
    """Either a Pydantic schema for the unit/app databags of 'this side' of the relation, which
    will be used to validate the relation databags in the output state, or:
    - 'skip' to skip schema validation altogether
    - 'empty' to have the schema validator assert that the databags should be empty.
    """
    input_state: Optional[State] = None
    """Initial state that this test should be run with."""

    def run(self, output_state: State):
        """Execute the test: that is, run the decorated validator against the output state."""
        return self.validator(output_state)


_TestCaseCacheType = Dict[Tuple["InterfaceNameStr", "VersionInt", Role], List[_InterfaceTestCase]]
# for each (interface_name, version, role) triplet: the list of all collected interface test cases.
REGISTERED_TEST_CASES: _TestCaseCacheType = defaultdict(list)


def get_registered_test_cases() -> _TestCaseCacheType:
    """The test cases that have been registered so far."""
    return REGISTERED_TEST_CASES


def get_interface_name_and_version(fn: Callable) -> Tuple[str, int]:
    f"""Return the interface name and version of a test case validator function.
    
    It assumes that the function is in a module whose path matches the following regex: 
    {INTF_NAME_AND_VERSION_REGEX}
    
    If that can't be matched, it will raise a InvalidTestCase.
    """

    file = inspect.getfile(fn)
    match = INTF_NAME_AND_VERSION_REGEX.findall(file)
    if len(match) != 1:
        raise InvalidTestCase(
            f"Can't determine interface name and version from test case location: {file}."
            rf"expecting a file path matching '/interfaces/(\w+)/v(\d+)/' "
        )
    interface_name, version_str = match[0]
    try:
        version_int = int(version_str)
    except TypeError:
        # overly cautious: the regex should already be only matching digits.
        raise InvalidTestCase(
            f"Unable to cast version {version_str} to integer. "
            f"Check file location: {file}."
        )
    return interface_name, version_int


def check_test_case_validator_signature(fn: Callable):
    """Verify the signature of a test case validator function.

    Will raise InvalidTestCase if:
    - the number of parameters is not exactly 1
    - the parameter is not positional only or positional/keyword

    Will pop a warning if the one argument is annotated with anything other than scenario.State
    (or no annotation).
    """
    sig = inspect.signature(fn)
    if not len(sig.parameters) == 1:
        raise InvalidTestCase(
            "interface test case validator expects exactly one "
            "positional argument of type State."
        )

    params = list(sig.parameters.values())
    par0 = params[0]
    if par0.kind not in (par0.POSITIONAL_OR_KEYWORD, par0.POSITIONAL_ONLY):
        raise InvalidTestCase(
            "interface test case validator expects the first argument to be positional."
        )

    if par0.annotation not in (par0.empty, State):
        logger.warning(
            "interface test case validator will receive a State as first and "
            "only positional argument."
        )


def interface_test_case(
        role: Union[Role, "RoleLiteral"],
        event: Union[str, Event],
        input_state: Optional[State] = None,
        name: str = None,
        schema: Union[
            DataBagSchema, SchemaConfig, "_SchemaConfigLiteral"
        ] = SchemaConfig.default,
):
    """Decorator to register a function as an interface test case.
    The decorated function must take exactly one positional argument of type State.

    Arguments:
    :param name: the name of the test. Will default to the decorated function's identifier.
    :param event: the event that this test is about.
    :param role: the interface role this test is about.
    :param input_state: the input state for this scenario test. Will default to the empty State().
    :param schema: the schema that the relation databags for the endpoint being tested should
        satisfy **after** the event has been processed.
    """
    if not isinstance(schema, DataBagSchema):
        schema = SchemaConfig(schema)

    def wrapper(fn: Callable[[State], None]):
        # validate that the function is a valid validator
        check_test_case_validator_signature(fn)

        # derive from the module the function is defined in what the
        # interface name and version are
        interface_name, version = get_interface_name_and_version(fn)

        role_ = Role(role)

        REGISTERED_TEST_CASES[(interface_name, version, role_)].append(
            _InterfaceTestCase(
                interface_name=interface_name,
                version=version,
                event=event,
                role=role_,
                validator=fn,
                name=name or fn.__name__,
                input_state=input_state,
                schema=schema,
            )
        )

    return wrapper


def _assert_case_plays(event: Event, state: State,
                       charm_type: Type["CharmBase"],
                       meta,
                       actions,
                       config) -> State:
    try:
        state_out = state.trigger(
            event,
            charm_type=charm_type,
            meta=meta,
            actions=actions,
            config=config,
        )
    except Exception as e:
        msg = f"Failed check 1: scenario errored out: ({type(e).__name__}){e}. Could not play scene."
        raise RuntimeError(msg) from e
    return state_out


def _assert_state_out_valid(state_out: State, test: "_InterfaceTestCase"):
    """Run the test's validator against the output state.

    Raise RuntimeError if any exception is raised by the validator.
    """
    try:
        test.run(state_out)
    except Exception as e:
        msg = f"Failed check 2: validating scene output: {e}"
        raise RuntimeError(msg) from e


def _assert_schema_valid(schema: DataBagSchema, relation: Relation) -> None:
    """Validate the relation databags against this schema.

    Raise RuntimeError if any exception is raised by the validator.
    """
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
        test: "_InterfaceTestCase",
        state_out: State,
        schema: DataBagSchema,
        interface_name: str
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
    for relation in [
        r for r in state_out.relations if r.interface == interface_name
    ]:
        try:
            _assert_schema_valid(schema=schema, relation=relation)
        except RuntimeError as e:
            errors.append(e.args[0])
    return errors


def run_test_case(
        test: "_InterfaceTestCase",
        schema: Optional["DataBagSchema"],
        event: Event,
        state: State,
        interface_name: str,
        # the charm type we're testing
        charm_type: Type["CharmBase"],
        # charm metadata yamls
        meta: Dict,
        config: Dict,
        actions: Dict,
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
        state_out = _assert_case_plays(event=event, state=state,
                                       charm_type=charm_type,
                                       meta=meta, config=config,
                                       actions=actions)
    except RuntimeError as e:
        errors.append(e.args[0])
        logger.info("scenario couldn't run: aborting test.")
        return errors

    logger.info("check 2: scenario output state validation")
    # todo: consistency check? or should we rely on scenario's?
    try:
        _assert_state_out_valid(state_out=state_out, test=test)
    except RuntimeError as e:
        errors.append(e.args[0])

    logger.info("check 3: databag schema validation")
    if not schema:
        logger.info("schema validation step skipped: no schema provided")
        return errors
    errors.extend(_assert_schemas_valid(test=test, state_out=state_out,
                                        schema=schema, interface_name=interface_name))
    return errors
