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
                 {"grpc_api_url": "http://10.10.0.17:8081",
                  "http_api_url": "http://10.10.0.17:8080",
                  "token": "test-token",
                  "token_secret_id": null,
                  "store_id": "01GK13VYZK62Q1T0X55Q2BHYD6",
                 }
             }

    RequirerSchema:
        unit: <empty>
        app: {"store_name": "test-store-name"}
"""
from typing import Dict, Optional
from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field, validator


class OpenFGAProviderData(BaseModel):
    grpc_api_url: str = Field(
        description=("The URL of the gRPC API."),
        title="gRPC URL",
    )
    http_api_url: str = Field(
        description=("The URL of the HTTP API."),
        title="HTTP URL",
    )
    token_secret_id: Optional[str] = Field(
        description=(
            "Secret ID of the preshared token to be used to connect to"
            " the OpenFGA service."
        ),
        title="Secret ID of the OpenFGA token",
        default=None,
    )
    token: Optional[str] = Field(
        description=(
            "The preshared token to be used to connect to the OpenFGA "
            "service, to be used when juju secrets are not available."
        ),
        title="The OpenFGA token",
        default=None,
    )
    store_id: Optional[str] = Field(
        description="ID of the authentication store that was created.",
        title="OpenFGA store ID",
        examples=["01GK13VYZK62Q1T0X55Q2BHYD6"],
        default=None,
    )

    @validator("token_secret_id", pre=True)
    def validate_token(cls, v: str, values: Dict) -> str:  # noqa: N805
        """Validate token_secret_id arg."""
        if not v and not values["token"]:
            raise ValueError("invalid scheme: neither of token and token_secret_id were defined")
        return v


class ProviderSchema(DataBagSchema):
    """Provider schema for OpenFGA."""

    app: OpenFGAProviderData


class OpenFGARequirerData(BaseModel):
    store_name: str = Field(
        description="The name of the authorization store.",
        title="Authorization store name",
        examples=["auth_store"],
    )


class RequirerSchema(DataBagSchema):
    """Requirer schema for OpenFGA."""

    app: OpenFGARequirerData
