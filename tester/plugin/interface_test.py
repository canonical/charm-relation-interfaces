import abc
import dataclasses
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

    schema: Optional[DataBagSchema] = None
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


def get_interface_schema(interface_name: str, role: Role) -> DataBagSchema:
    pass


def get_interface_name_and_version(fn: Callable) -> Tuple[str, int]:
    pass


def interface_test_case(role: Union[Role, "RoleLiteral"],
                        event: Union[str, Event],
                        input_state: Optional[State] = None,
                        schema: Optional[DataBagSchema] = _NotGiven):
    """Decorator to register a function as an interface test case."""

    def wrapper(fn:Callable[[State], None]):
        interface_name, version = get_interface_name_and_version(fn)

        role_ = Role(role)
        schema_ = get_interface_schema(interface_name, role_) if schema is _NotGiven else schema
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
                schema=schema_
            )
        )

    return wrapper
