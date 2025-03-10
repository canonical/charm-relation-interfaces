"""This file defines the schemas for the provider and requirer sides connect_client interface.

It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from pydantic import BaseModel, Field

from interface_tester.schema_base import DataBagSchema


PLUGIN_URL_NOT_REQUIRED = "NOT-REQUIRED"


class ConnectProviderData(BaseModel):
    username: str = Field(
        description="Username to be used on the Kafka Connect REST endpoint(s)",
        examples=["relation-7"],
    )
    password: str = Field(
        description="Password to be used on the Kafka Connect REST endpoint(s)",
        examples=["6Kt3niByjltswXvaO43N9P9vbyUvoBcS"],
    )
    endpoints: str = Field(
        description="A comma-separated list of Kafka Connect REST endpoint(s), including the protocol (either `http` or `https`)",
        examples=[
            "http://10.1.1.100:8083,http://10.1.1.101:8083,http://10.1.1.102:8083"
        ],
    )


class ConnectRequirerData(BaseModel):
    plugin_url: str = Field(
        description=f'URL at which the plugins required by this client are served as a single Tarball. If not required, the requirer should place the sentinel value "{PLUGIN_URL_NOT_REQUIRED}"',
        alias="plugin-url",
        examples=["http://10.1.1.200:8080/route/to/plugins", PLUGIN_URL_NOT_REQUIRED],
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of the `connect_client` interface."""

    app: ConnectProviderData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of the `connect_client` interface."""

    app: ConnectRequirerData
