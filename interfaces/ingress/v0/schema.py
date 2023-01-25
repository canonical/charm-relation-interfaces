import yaml
from pydantic import BaseModel, Json, AnyHttpUrl, validator

from interface_test import DataBagSchema


class Url(BaseModel):
    url: AnyHttpUrl


class MyProviderAppData(BaseModel):
    ingress: Url

    @validator('ingress', pre=True)
    def decode_ingress(cls, ingress):
        return yaml.safe_load(ingress)


class MyRequirerAppData(BaseModel):
    port: Json[int]
    host: str
    model: str
    name: str


class ProviderSchema(DataBagSchema):
    app: MyProviderAppData


class RequirerSchema(DataBagSchema):
    app: MyRequirerAppData
