# Copyright 2023 Canonical
# See LICENSE file for licensing details.
"""This file defines the schemas for the provider and consumer sides of the ingress interface.

It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- ConsumerSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {"ingress":
                 {"url":  "http://foo.bar:80/model_name-app_name"}
             }

    ConsumerSchema:
        unit: <empty>
        app: {"name": "app-name",
              "host": "hostname",
              "port": 4242,
              "model": "model-name"
              }
"""

import yaml
from pydantic import BaseModel, Json, AnyHttpUrl, validator

from interfaces.schema_base import DataBagSchema


class Url(BaseModel):
    url: AnyHttpUrl


class MyProviderAppData(BaseModel):
    ingress: Url

    @validator('ingress', pre=True)
    def decode_ingress(cls, ingress):
        return yaml.safe_load(ingress)


class MyRequirerAppData(BaseModel):
    port: Json[int]  # The port the application wishes to be exposed.
    host: str  # Hostname the application wishes to be exposed.
    model: str  # the model the application is in.
    name: str  # the name of the application requesting ingress.


class ProviderSchema(DataBagSchema):
    """Provider schema for Ingress."""
    app: MyProviderAppData


class RequirerSchema(DataBagSchema):
    """Requirer schema for Ingress."""
    app: MyRequirerAppData
