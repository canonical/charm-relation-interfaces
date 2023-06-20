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
from pydantic import BaseModel, Field, IPvAnyAddress


class OpenFGAProviderData(BaseModel):
    address: IPvAnyAddress = Field(
        description="The address of the OpenFGA service.",
        title="OpenFGA address",
        examples=["10.10.4.1"],
    )
    port: int = Field(
        description="Port on which the OpenFGA service is listening (HTTP).",
        title="OpenFGA port",
        examples=[8080],
    ) 
    scheme: str = Field(
        description="Scheme to be used to connect to the OpenFGA service.",
        title="OpenFGA scheme",
        examples=["http","https"],
    )
    token_secret_id: str = Field(
        description="Secret ID of the preshared token to be used to connect to the OpenFGA service.",
        title="Secret ID of the OpenFGA token",
    )

    store_id: str = Field(
        description="ID of the authentication stored that was created.",
        title="OpenFGA store ID",
        examples=["01GK13VYZK62Q1T0X55Q2BHYD6"],
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for OpenFGA."""
    app: OpenFGAProviderData


class OpenFGARequirerData(BaseModel):
    store_name: str = Field(
        description="The name of the authentication store.",
        title="Authorization store name",
        examples=["auth_store"],
    )


class RequirerSchema(DataBagSchema):
    """Requirer schema for OpenFGA."""
    app: OpenFGARequirerData
