# Copyright 2025 Canonical
# See LICENSE file for licensing details.
"""This file defines the schema for the provider side of the wazuh-api-client interface.

It exposes one interfaces.schema_base.DataBagSchema subclass called:
- ProviderSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {"wazuh-api-client":
                 {
                    "endpoint": "10.180.162.200:55000",
                    "secret-user": "secret://59060ecc-0495-4a80-8006-5f1fc13fd783/cjqub6vubg2s77p3nio0",
                }
             }
"""
from interface_tester.schema_base import DataBagSchema
from pydantic import AnyHttpUrl, BaseModel, Field


class WazuhApiclientProviderData(BaseModel):
    endpoint: AnyHttpUrl = Field(
        description="Endpoint used to connect to the API.",
        title="Endpoint",
        examples=["https://10.180.162.200:55000"],
    )
    secret_user: str = Field(
        min_length=1,
        description="The secret ID containing the user and password for the API.",
        title="User secret",
        examples=["secret://59060ecc-0495-4a80-8006-5f1fc13fd783/cjqub6vubg2s77p3nio0"],
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for Wazuh API client."""

    app: WazuhApiclientProviderData


class RequirerSchema(DataBagSchema):
    """Requirer schema for Wazuh API client."""
