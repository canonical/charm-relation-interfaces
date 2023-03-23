import abc
import dataclasses
import inspect
import logging
import re
import typing
from collections import defaultdict
from enum import Enum
from typing import Callable, Dict, List, Literal, Optional, Tuple, Union

from interfaces.schema_base import DataBagSchema
from scenario import Event, Relation, State

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
    interface_name: str
    version: int
    event: Union[Event, str]
    role: Role
    name: str
    validator: Callable[[State], None]

    schema: Union[DataBagSchema, SchemaConfig] = SchemaConfig.default
    input_state: Optional[State] = None

    def run(self, output_state: State):
        """Execute the test: that is, run the decorated validator against the output state."""
        return self.validator(output_state)

    def validate_schema(self, relation: Relation):
        """Validate the"""
        if not self.schema:
            return
        return self.schema.validate(
            {
                "unit": relation.local_unit_data,
                "app": relation.local_app_data,
            }
        )


REGISTERED_TEST_CASES: Dict[
    Tuple["InterfaceNameStr", "VersionInt", Role], List[_InterfaceTestCase]
] = defaultdict(list)


def get_registered_test_cases():
    """The test cases that have been registered so far."""
    return REGISTERED_TEST_CASES


def get_interface_name_and_version(fn: Callable) -> Tuple[str, int]:
    file = inspect.getfile(fn)
    match = INTF_NAME_AND_VERSION_REGEX.findall(file)
    if len(match) != 1:
        raise ValueError(
            f"Can't determine interface name and version from test case location: {file}."
            rf"expecting a file path matching '/interfaces/(\w+)/v(\d+)/' "
        )
    interface_name, version_str = match[0]
    try:
        version_int = int(version_str)
    except TypeError:
        raise InvalidTestCase(
            f"Unable to cast version {version_str} to integer. "
            f"Check file location: {file}."
        )
    return interface_name, version_int


def check_signature(fn):
    sig = inspect.signature(fn)
    if not len(sig.parameters) >= 1:
        raise InvalidTestCase(
            "interface test case validator expects exactly one "
            "positional argument of type State."
        )

    par0 = list(sig.parameters.values())[0]
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
    :param name: the name of the test. Will default to the decorated function's name.
    :param event: the event that this test is about.
    :param role: the interface role this test is about.
    :param input_state: the input state for this scenario test. Will default to the empty State().
    :param schema: the schema that the relation databags for the endpoint being tested should
        satisfy **after** the event has been processed.
    """
    if not isinstance(schema, DataBagSchema):
        schema = SchemaConfig(schema)

    def wrapper(fn: Callable[[State], None]):
        check_signature(fn)

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
