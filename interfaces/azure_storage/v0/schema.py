"""This file defines the schemas for the provider and requirer sides of the zookeeper_client interface.
It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""
from enum import Enum
from pathlib import Path
from typing import List

from interface_tester.schema_base import DataBagSchema
from pydantic import (
    BaseModel,
    Field,
    SecretStr
)


class ConnectionProtocolEnum(str, Enum):
    blob_storage_insecure = "wasb"
    blob_storage_secure = "wasbs"
    adls_gen2_insecure = "abfs"
    adls_gen2_secure = "abfss"


class AzureStorageProviderAppData(BaseModel):
    container: str = Field(
        description="The name of the Azure storage container provided by the provider.",
        examples=["mycontainer"],
        title="Container",
    )
    
    storage_account : str = Field(
        description="The name of Azure storage account.",
        examples=["test-storage-account"],
        title="Storage account",
    )

    connection_protocol: ConnectionProtocolEnum = Field(
        description="The connection protocol to be used to connect to Azure Storage.",
        examples=["wasb", "wasbs", "abfs", "abfss"],
        default=ConnectionProtocolEnum.adls_gen2_secure,
        title="Connection protocol",
    )

    secret_key: SecretStr = Field(
        description="Secret key corresponding to the storage account for connecting to the object storage.",
        examples=["random-secret-key"],
        title="Secret key",
    )

    path: Path = Field(
        description="The path inside the container to store objects.",
        examples=["foo/bar"],
        title="Path"
    )

    endpoint: str = Field(
        description="The endpoint corresponding to the specific container and storage account.",
        examples=["abfss://test-container@test-account.dfs.core.windows.net/"],
        title="Endpoint URL"
    )


class AzureStorageRequirerAppData(BaseModel):
    container: str = Field(
        description="The name of the container that's requested by the requirer.",
        examples=["mycontainer"],
        title="container",
    )

    requested_secrets: List[str] = Field(
        alias="requested-secrets",
        description="Any provider field which should be transfered as Juju Secret",
        examples=[["username", "password", "tls-ca", "uris"]],
        title="Requested secrets",
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: AzureStorageProviderAppData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    app: AzureStorageRequirerAppData