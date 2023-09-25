"""This file defines the schemas for the provider and requirer sides of this relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from typing import Mapping

from pydantic import BaseModel, Field, Json

from interface_tester.schema_base import DataBagSchema


class VaultKvProviderSchema(BaseModel):
    vault_url: str = Field(description="The URL of the Vault server to connect to.")
    mount: str = Field(
        description=(
            "The KV mount available for the requirer application, "
            "respecting the pattern 'charm-<requirer app>-<user provided suffix>'."
        )
    )
    ca_certificate: str = Field(
        description="The CA certificate to use when validating the Vault server's certificate."
    )
    credentials: Json[Mapping[str, str]] = Field(
        description=(
            "Mapping of unit name and credentials for that unit."
            " Credentials are a juju secret containing a 'role-id' and a 'role-secret-id'."
        )
    )


class AppVaultKvRequirerSchema(BaseModel):
    mount_suffix: str = Field(
        description="Suffix to append to the mount name to get the KV mount."
    )


class UnitVaultKvRequirerSchema(BaseModel):
    egress_subnet: str = Field(description="Egress subnet to use, in CIDR notation.")
    nonce: str = Field(
        description=(
            "Uniquely identifying value for this unit."
            " `secrets.token_hex(16)` is recommended."
        )
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: VaultKvProviderSchema


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    app: AppVaultKvRequirerSchema
    unit: UnitVaultKvRequirerSchema
