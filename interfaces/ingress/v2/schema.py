# Copyright 2023 Canonical
# See LICENSE file for licensing details.
"""This file defines the schemas for the provider and requirer sides of the ingress interface.

It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {"ingress":
                 {"url":  "http://foo.bar:80/model_name-app_name"}
             }

    RequirerSchema:
        unit: {
              "name": "app-name",
              "host": "hostname"
              }
        app: {
              "port": 4242,
              "model": "model-name"
              }
"""
import yaml
from pydantic import BaseModel, AnyHttpUrl, validator, Field

from interface_tester.schema_base import DataBagSchema


class Url(BaseModel):
    url: AnyHttpUrl


class MyProviderData(BaseModel):
    ingress: Url

    @validator('ingress', pre=True)
    def decode_ingress(cls, ingress):
        return yaml.safe_load(ingress)


class ProviderSchema(DataBagSchema):
    """Provider schema for Ingress."""
    app: MyProviderData


class IngressRequirerAppData(BaseModel):
    host: str = Field(description="Hostname the application wishes to be exposed.")
    model: str = Field(description="The model the application is in.")


class IngressRequirerUnitData(BaseModel):
    port: str = Field(description="The port the unit wishes to be exposed. Stringified int.")
    name: str = Field(description="the name of the unit requesting ingress.")


class RequirerSchema(DataBagSchema):
    """Requirer schema for Ingress."""
    app: IngressRequirerAppData
    unit: IngressRequirerUnitData
