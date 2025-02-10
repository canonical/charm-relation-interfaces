"""This file defines the schemas for the provider and requirer sides of the zookeeper_client interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from typing import TypeAlias

from interface_tester.schema_base import DataBagSchema
from pydantic import (
    BaseModel,
    Field,
)


Endpoints: TypeAlias = str


class ZooKeeperProviderAppData(BaseModel):
    database: str = Field(
        description="The parent chroot zNode granted to the requirer",
        examples=["/myappB"],
        title="zNode",
    )

    endpoints: Endpoints = Field(
        description="A comma-seperated list of ZooKeeper server and ports",
        examples=["10.141.78.133:2181,10.141.78.50:2181,10.141.78.45:2181"],
        title="ZooKeeper endpoints",
    )

    secret_user: str = Field(
        alias="secret-user",
        description="The credentials to connect to ZooKeeper. The secret contains [user,password,uris].",
        examples=["secret://59060ecc-0495-4a80-8006-5f1fc13fd783/cjqub6vubg2s77p3nio0"],
        title="Credentials Secret Name",
    )

    secret_tls: str | None = Field(
        None,
        alias="secret-tls",
        description="The name of the TLS secret to use. Leaving this empty will configure a client with TLS disabled. The secret contains [tls].",
        examples=["secret://59060ecc-0495-4a80-8006-5f1fc13fd783/cjqub7fubg2s77p3niog"],
        title="TLS Secret Name",
    )


class ZooKeeperRequirerAppData(BaseModel):
    database: str = Field(
        description="The parent chroot zNode requested by the requirer",
        examples=["/myappA"],
        title="zNode",
    )

    extra_user_roles: str | None = Field(
        None,
        alias="extra-user-roles",
        description="ACL string representation for the parent chroot",
        examples=["cdrwa"],
        title="User roles",
    )

    requested_secrets: list[str] = Field(
        alias="requested-secrets",
        description="Any provider field which should be transfered as Juju Secret",
        examples=[["username", "password", "tls-ca", "uris"]],
        title="Requested secrets",
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: ZooKeeperProviderAppData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    app: ZooKeeperRequirerAppData
