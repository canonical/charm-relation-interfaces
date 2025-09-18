"""This file defines the schemas for the provider and requirer sides of the azure_service_principal interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from pathlib import Path
from typing import List

from interface_tester.schema_base import DataBagSchema
from pydantic import (
    BaseModel,
    Field,
    SecretStr
)


class AzureServicePrincipalProviderAppData(BaseModel):
    """Credentials for an Azure Service Principal."""
    
    subscription_id: str = Field(
        description="The unique identifier for an Azure subscription.",
        examples=["12345678-1234-1234-1234-1234567890ab"],
        title="Subscription ID",
    )
    
    tenant_id: str = Field(
        description="The unique identifier of the Azure Active Directory (Entra ID) tenant.",
        examples=["87654321-4321-4321-4321-ba0987654321"],
        title="Tenant ID",
    )

    client_id: str = Field(
        description="The Application (client) ID for the service principal.",
        examples=["a1b2c3d4-e5f6-a7b8-c9d0-e1f2a3b4c5d6"],
        title="Client ID",
    )

    client_secret: SecretStr = Field(
        description="The client secret for the service principal, used for authentication.",
        examples=["aBcDeFgHiJkLmNoPqRsTuVwXyZ123456-~7890_"],
        title="Client Secret",
    )


class AzureServicePrincipalRequirerAppData(BaseModel):
    requested_secrets: List[str] = Field(
        alias="requested-secrets",
        description="Any provider field which should be transfered as a Juju secret",
        examples=[["client-id", "client-secret"]],
        title="Requested secrets",
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: AzureServicePrincipalProviderAppData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    app: AzureServicePrincipalRequirerAppData
