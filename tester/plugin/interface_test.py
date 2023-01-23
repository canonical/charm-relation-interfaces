import abc
from typing import Literal, Union, Dict, Any

import jsonschema as jsonschema
from scenario.structs import State, Event, RelationSpec


class InterfaceTestCase(abc.ABC):
    INPUT_STATE: State = None

    @property
    @abc.abstractmethod
    def ROLE(self) -> Literal['provider', 'requirer']:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def EVENT(self) -> Union[str, Event]:
        raise NotImplementedError()

    @staticmethod
    @abc.abstractmethod
    def validate(output_state: State):
        raise NotImplementedError("validate")

    @staticmethod
    def validate_schema(relation: RelationSpec, schema: Dict[Any, Any]):
        # todo: consider if this behaviour should be configurable.
        valid = [None, None]

        if app_data := relation.local_app_data:
            jsonschema.validate(
                app_data,
                schema
            )
            valid[0] = True

        if unit_data := relation.local_unit_data:
            jsonschema.validate(
                unit_data,
                schema
            )
            valid[1] = True

        return valid
