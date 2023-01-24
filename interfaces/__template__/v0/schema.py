from typing import List

from pydantic import Json, BaseModel

from interface_test import DataBagSchema


class Url(BaseModel):
    addr: str


class MyProviderAppData(BaseModel):
    foo: Json[int]
    bar: str
    baz: Json[List[float]]


provider_schema = DataBagSchema(app=MyProviderAppData)
requirer_schema = DataBagSchema(unit=MyRequirerUnitData)
