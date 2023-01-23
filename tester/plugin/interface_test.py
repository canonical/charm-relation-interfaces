import abc
from typing import Literal, Union

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

    @abc.abstractmethod
    def validate(self, output_state: State):
        raise NotImplementedError("validate")

    def validate_schema(self, output_state: State):
        pass
        # todo use self.role + ../schemas/{role}.json to validate databag contents.
        #  run this function after validate() output_state is dedup'ed from validate's.
