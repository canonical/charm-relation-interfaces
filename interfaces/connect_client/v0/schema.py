"""This file defines the schemas for the provider and requirer sides  of `connect_client` charm relation interface.

It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from typing import List, Optional

from pydantic import BaseModel, Field

from interface_tester.schema_base import DataBagSchema


PLUGIN_URL_NOT_REQUIRED = "NOT-REQUIRED"


class ConnectProviderData(BaseModel):
    endpoints: str = Field(
        description="A comma-separated list of Kafka Connect REST endpoint(s), including the protocol (either `http` or `https`)",
        examples=[
            "http://10.1.1.100:8083,http://10.1.1.101:8083,http://10.1.1.102:8083"
        ],
        title="Kafka Connect Endpoints"
    )
    secret_user: str = Field(
        alias="secret-user",
        description="The credentials to connect to Kafka Connect. The secret contains [username,password].",
        examples=["secret://59060ecc-0495-4a80-8006-5f1fc13fd783/cjqub6vubg2s77p3nio0"],
        title="Credentials Secret Name",
    )
    secret_tls: Optional[str] = Field(
        None,
        alias="secret-tls",
        description="The name of the TLS secret to use. Leaving this empty will configure a client with TLS disabled. The secret contains [tls,tls-ca].",
        examples=["secret://59060ecc-0495-4a80-8006-5f1fc13fd783/cjqub7fubg2s77p3niog"],
        title="TLS Secret Name",
    )



class ConnectRequirerData(BaseModel):
    plugin_url: str = Field(
        description=f'URL at which the plugins required by this client are served as a single Tarball. If not required, the requirer should place the sentinel value "{PLUGIN_URL_NOT_REQUIRED}"',
        alias="plugin-url",
        examples=["http://10.1.1.200:8080/route/to/plugins", PLUGIN_URL_NOT_REQUIRED],
        title="Plugin URL",
    )
    requested_secrets: List[str] = Field(
        alias="requested-secrets",
        description="Any provider field which should be transfered as Juju Secret",
        examples=[["username", "password", "tls-ca"]],
        title="Requested secrets",
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of the `connect_client` interface."""

    app: ConnectProviderData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of the `connect_client` interface."""

    app: ConnectRequirerData
