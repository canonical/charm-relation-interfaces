"""This file defines the schemas for the provider and requirer sides of this relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from typing import Mapping

from pydantic import BaseModel, Field, Json

from interface_tester.schema_base import DataBagSchema


class UnitCredentialsSchema(BaseModel):
    role_id: str = Field(description="The role ID to use to authenticate to Vault.")
    role_secret_id: str = Field(
        description="The role secret ID to use to authenticate to Vault."
    )


class CredentialsSchema(BaseModel):
    __root__: Mapping[str, UnitCredentialsSchema] = Field("Units' credentials")


class VaultKvProviderSchema(BaseModel):
    vault_url: str = Field(description="The URL of the Vault server to connect to.")
    kv_mountpoint: str = Field(description="The mountpoint of the KV store to use.")
    credentials: Json[CredentialsSchema] = Field(
        description="The credentials to use to authenticate to Vault."
    )


class AppVaultKvProviderSchema(BaseModel):
    secret_backend: str = Field("The name of the secret backend to use.")


class UnitVaultKvRequirerSchema(BaseModel):
    egress_subnet: str = Field("Egress subnet to use.")


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: VaultKvProviderSchema


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    app: AppVaultKvProviderSchema
    unit: UnitVaultKvRequirerSchema
