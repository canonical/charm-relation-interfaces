from typing import Dict

from pydantic import BaseModel, Json

from interface_test import DataBagSchema


class Url(BaseModel):
    addr: str


class MyProviderAppData(BaseModel):
    urls: Json[Dict[str, Url]]


class MyRequirerUnitData(BaseModel):
    port: int
    host: str
    model: str
    name: str


class ProviderSchema(DataBagSchema):
    app: MyProviderAppData


class RequirerSchema(DataBagSchema):
    unit: MyRequirerUnitData
