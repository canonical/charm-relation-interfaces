"""This file defines the schemas for the provider and requirer sides of the zookeeper_client interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from typing import Annotated, TypeAlias

from interface_tester.schema_base import DataBagSchema
from pydantic import (
    # AfterValidator,
    BaseModel,
    Field,
    IPvAnyAddress,
    conint,
)


class URI(BaseModel):
    ip: IPvAnyAddress
    port: conint(ge=0, le=65535) | None

    def __init__(self, value: str) -> None:
        ip, _, port = value.partition(":")
        if not port:
            port = None
        super().__init__(ip=ip, port=port)


def parse_endpoints(value: str):
    uris, _, znode = value.partition("/")
    [URI(val) for val in uris.split(",")]


# Endpoints = Annotated[str, AfterValidator(parse_endpoints)]
Endpoints: TypeAlias = str


class ZookeeperProviderAppData(BaseModel):
    database: str = Field(
        description="The parent chroot zNode granted to the requirer",
        examples=["/myappB"],
        title="zNode",
    )

    endpoints: Endpoints = Field(
        description="A comma-seperated list of ZooKeeper server uris, and parent chroot zNode",
        examples=["10.141.78.133:2181,10.141.78.50:2181,10.141.78.45:2181/myappB"],
        title="ZooKeeper URIs",
    )

    secret_user: str = Field(
        alias="secret-user",
        description="",
        examples=["secret://59060ecc-0495-4a80-8006-5f1fc13fd783/cjqub6vubg2s77p3nio0"],
        title="Credentials Secret Name",
    )

    secret_tls: str | None = Field(
        None,
        alias="secret-tls",
        description="The name of the TLS secret to use. Leaving this empty will configure a client with TLS disabled.",
        examples=["secret://59060ecc-0495-4a80-8006-5f1fc13fd783/cjqub7fubg2s77p3niog"],
        title="TLS Secret Name",
    )


class ZookeeperRequirerAppData(BaseModel):
    database: str = Field(
        description="The parent chroot zNode requested by the requirer",
        examples=["/myappA"],
        title="zNode",
    )

    requested_secrets: list[str] = Field(
        alias="requested-secrets",
        description="Any provider field which should be transfered as Juju Secret",
        examples=[["username", "password", "tls-ca", "uris"]],
        title="Requested secrets",
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: ZookeeperProviderAppData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    app: ZookeeperRequirerAppData
