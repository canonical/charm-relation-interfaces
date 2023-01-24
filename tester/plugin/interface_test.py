import abc
from typing import Literal, Union, Optional

from pydantic import BaseModel
from scenario.structs import State, Event, RelationSpec


class DataBagSchema(BaseModel):
    unit: Optional[BaseModel] = None
    app: Optional[BaseModel] = None


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
    def validate_schema(relation: RelationSpec, schema: DataBagSchema):
        return schema.validate({
            "unit": relation.local_unit_data,
            "app": relation.local_app_data,
        })
