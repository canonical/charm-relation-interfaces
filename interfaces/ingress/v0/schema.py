import json
from typing import Dict
from urllib.parse import urlparse
from pydantic import BaseModel, Json, AnyHttpUrl, validator

from interface_test import DataBagSchema


class Url(BaseModel):
    url: AnyHttpUrl


class MyProviderAppData(BaseModel):
    urls: Json[Dict[str, Url]]

    @validator('urls')
    def validate_urls(cls, urls):
        if not urls:
            return

        for unit_name in urls.keys():
            a, b, c = unit_name.rpartition('/')
            if not a and b and c:
                raise ValueError(f'invalid unit name: {unit_name}')
            assert c.isdigit(), f'invalid unit number: {c} not an integer'
            assert a.replace('-', '').replace('_', '').isalpha(), f"invalid app name: {a} is not a valid juju app name"


class MyRequirerAppData(BaseModel):
    port: Json[int]
    host: str
    model: str
    name: str


class ProviderSchema(DataBagSchema):
    app: MyProviderAppData


class RequirerSchema(DataBagSchema):
    app: MyRequirerAppData
