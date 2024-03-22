"""This file defines the schemas for the provider and requirer sides of this relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field


class VaultTransitProviderSchema(BaseModel):
    address: str = Field(description="The address of the Vault server to connect to.")
    token_secret_id: str = Field(
        description=(
            "The secret id of the Juju secret which stores is token for authenticating with the Vault server."
        )
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: VaultTransitProviderSchema
