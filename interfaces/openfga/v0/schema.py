# Copyright 2023 Canonical
# See LICENSE file for licensing details.
"""This file defines the schemas for the provider and requirer sides of the openfga interface.

It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {"openfga":
                 {"address":  "10.10.0.17",
                  "port": "8080",
                  "scheme": "http",
                  "token": "test-token",
                  "store_id": "01GK13VYZK62Q1T0X55Q2BHYD6",
                 }
             }

    RequirerSchema:
        unit: <empty>
        app: {"store_name": "test-store-name"}
"""
from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel


class OpenFGAProviderData(BaseModel):
    address: str # The address of the OpenFGA service.
    port: str # Port on which the OpenFGA service is listening (HTTP).
    scheme: str # Scheme to be used to connect to the OpenFGA service.
    token: str # Preshared token to be used to connect to the OpenFGA service.
    store_id: str # ID of the authentication stored that was created.


class ProviderSchema(DataBagSchema):
    """Provider schema for OpenFGA."""
    app: OpenFGAProviderData


class OpenFGARequirerData(BaseModel):
    store_name: str  # The name of the authentication store.


class RequirerSchema(DataBagSchema):
    """Requirer schema for OpenFGA."""
    app: OpenFGARequirerData
