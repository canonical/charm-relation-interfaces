import abc
import dataclasses
import inspect
import re
import typing
from collections import defaultdict
from enum import Enum
from typing import Literal, Optional, Union, Dict, Callable, List, Tuple

from scenario import Event, Relation, State

from interfaces.schema_base import DataBagSchema

if typing.TYPE_CHECKING:
    InterfaceNameStr = str
    VersionInt = int
    RoleLiteral = Literal["requirer", "provider"]
    _SchemaConfigLiteral = Literal["default", "skip", "empty"]

INTF_NAME_AND_VERSION_REGEX = re.compile(r"/interfaces/(\w+)/v(\d+)/")


class SchemaConfig(str, Enum):
    """Class used to program the schema validator run that is paired with each test case."""

    default = 'default'
    """Use this value if you want the test case to validate the output state's databags with the default schema."""
    skip = 'skip'
    """Use this value if you want the test case skip schema validation altogether."""
    empty = 'empty'
    """Use this value if you want the databag validator to assert that the databags are empty."""


class Role(str, Enum):
    provider = 'provider'
    requirer = 'requirer'


@dataclasses.dataclass
class _InterfaceTestCase:
    interface_name: str
    version: int
    event: Event
    role: Role
    name: str
    validator: Callable[[State], None]

    schema: Union[DataBagSchema, SchemaConfig] = SchemaConfig.default
    input_state: Optional[State] = None

    def run(self, output_state: State):
        return self.validator(output_state)

    def validate_schema(self, relation: Relation):
        if not self.schema:
            return
        return self.schema.validate(
            {
                "unit": relation.local_unit_data,
                "app": relation.local_app_data,
            }
        )


REGISTERED_TEST_CASES: Dict[Tuple["InterfaceNameStr", "VersionInt", Role], List[_InterfaceTestCase]] = defaultdict(list)
_NotGiven = object()


def get_interface_name_and_version(fn: Callable) -> Tuple[str, int]:
    file = inspect.getfile(fn)
    match = INTF_NAME_AND_VERSION_REGEX.findall(file)
    if len(match) != 1:
        raise ValueError(f"Can't determine interface name and version from test case location: {file}."
                         fr"expecting a file path matching '/interfaces/(\w+)/v(\d+)/' ")
    interface_name, version_str = match[0]
    try:
        version_int = int(version_str)
    except TypeError:
        raise ValueError(f'Unable to cast version {version_str} to integer. '
                         f'Check file location: {file}.')
    return interface_name, version_int


def interface_test_case(
        role: Union[Role, "RoleLiteral"],
        event: Union[str, Event],
        input_state: Optional[State] = None,
        schema: Union[DataBagSchema, SchemaConfig, "_SchemaConfigLiteral"] = SchemaConfig.default
):
    """Decorator to register a function as an interface test case."""
    if not isinstance(schema, DataBagSchema):
        schema = SchemaConfig(schema)

    def wrapper(fn: Callable[[State], None]):
        interface_name, version = get_interface_name_and_version(fn)

        role_ = Role(role)
        event_ = Event(event) if isinstance(event, str) else event

        REGISTERED_TEST_CASES[(interface_name, version, role_)].append(
            _InterfaceTestCase(
                interface_name=interface_name,
                version=version,
                event=event_,
                role=role_,
                validator=fn,
                name=fn.__name__,
                input_state=input_state,
                schema=schema
            )
        )

    return wrapper
