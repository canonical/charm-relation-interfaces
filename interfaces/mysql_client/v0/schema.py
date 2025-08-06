"""This file defines the schemas for the provider and requirer sides of the mysql_client interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from typing import List, Optional

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field


class MySQLProviderData(BaseModel):
    """The databag for the provider side of this interface."""

    database: str = Field(
        description="The database name delivered by the provider. Might not be the same as requested by the requirer",
        examples=["myapp"],
        title="Database name",
    )

    username: str = Field(
        description="Username for connecting to the requested database",
        examples=["relation-14"],
        title="Database user name",
    )

    password: str = Field(
        description="Password for connecting to the requested database",
        examples=["alphanum-32byte-random"],
        title="Database user password",
    )

    endpoints: str = Field(
        description="A list of database endpoints used to connect to the database",
        examples=["unit-1:port,unit-2:port"],
        title="Database endpoints",
    )

    uris: Optional[str] = Field(
        None,
        description="A list of connection strings in URI format used to connect to the database",
        examples=["mysql://user:pass@host:port/mydb"],
        title="Database URIs",
    )

    read_only_endpoints: Optional[str] = Field(
        None,
        alias="read-only-endpoints",
        description="A list of endpoints used to connect to the database in read-only mode",
        examples=["unit-1:port,unit-2:port"],
        title="Database read-only endpoints",
    )

    read_only_uris: Optional[str] = Field(
        None,
        alias="read-only-uris",
        description="A list of connection strings in URI format used to connect to the read only endpoint of the database",
        examples=["mysql://user:pass@host:port/mydb"],
        title="Database read-only URIs",
    )

    version: Optional[str] = Field(
        None,
        description="The version of the database engine",
        examples=["8.0.27-18"],
        title="Version",
    )

    entity_name: Optional[str] = Field(
        None,
        alias="entity-name",
        description="Name for the requested custom entity",
        examples=["custom-role"],
        title="Entity name",
    )

    entity_password: Optional[str] = Field(
        None,
        alias="entity-password",
        description="Password for the requested custom entity",
        examples=["alphanum-32byte-random"],
        title="Entity password",
    )


class MySQLRequirerData(BaseModel):
    """The databag for the requirer side of this interface."""

    database: str = Field(
        description="The database name requested by the requirer",
        examples=["myapp"],
        title="Database name",
    )

    requested_secrets: List[str] = Field(
        alias="requested-secrets",
        description="Any provider field which should be transferred as Juju Secret",
        examples=[["username", "password"]],
        title="Requested secrets",
    )

    extra_user_roles: Optional[str] = Field(
        None,
        alias="extra-user-roles",
        description="Any extra user roles requested by the requirer",
        examples=["default,admin"],
        title="Extra user roles",
    )

    extra_group_roles: Optional[str] = Field(
        None,
        alias="extra-group-roles",
        description="Any extra group roles requested by the requirer",
        examples=["charmed_read"],
        title="Extra group roles",
    )

    entity_type: Optional[str] = Field(
        None,
        alias="entity-type",
        description="Type of the requested entity (user / group)",
        examples=["USER", "GROUP"],
        title="Entity type",
    )

    entity_permissions: Optional[str] = Field(
        None,
        alias="entity-permissions",
        description="List of permissions to assign to the custom entity, in JSON format",
        examples=["[{\"resource_name\": \"items\", \"resource_type\": \"TABLE\", \"privileges\": [\"SELECT\"]}]"],
        title="Entity permissions",
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: MySQLProviderData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    app: MySQLRequirerData
