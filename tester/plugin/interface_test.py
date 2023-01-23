import abc
from typing import Literal, Union, Dict, Any

import jsonschema as jsonschema
from scenario.structs import State, Event


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
    def validate_schema(output_state: State, schema: Dict[Any, Any]):

        # if there is data: validate it.
        # if there is no data: all is valid.
        # todo: consider if this behaviour should be configurable.

        jsonschema.validate(
            schema
        )
        # todo use self.role + ../schemas/{role}.json to validate databag contents.
        #  run this function after validate() output_state is dedup'ed from validate's.
