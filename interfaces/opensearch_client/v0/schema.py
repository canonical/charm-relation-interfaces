"""This file defines the schemas for the provider and requirer sides of the opensearch_client interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from typing import List, Optional

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field


class OpenSearchProviderData(BaseModel):
    """The databag for the provider side of this interface."""

    index: str = Field(
        description="The index that has been made available to the relation user. Name defined in the Requirer's index field",
        examples=["myindex"],
        title="Index name",
    )

    username: str = Field(
        description="Username for connecting to the requested index",
        examples=["opensearch-client_0_user"],
        title="Relation user name",
    )

    password: str = Field(
        description="Password for connecting to the requested index",
        examples=["alphanum-32byte-random"],
        title="Relation user password",
    )

    endpoints: str = Field(
        description="A list of endpoints used to connect to the index",
        examples=["unit-1:9200,unit-2:9200"],
        title="Relation endpoints",
    )

    version: Optional[str] = Field(
        None,
        description="The version of OpenSearch",
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


class OpenSearchRequirerData(BaseModel):
    """The databag for the requirer side of this interface."""

    index: str = Field(
        description="The index name requested by the requirer",
        examples=["myindex"],
        title="Index name",
    )

    requested_secrets: List[str] = Field(
        alias="requested-secrets",
        description="Any provider field which should be transferred as Juju Secret",
        examples=[["username", "password"]],
        title="Requested secrets",
    )

    extra_user_roles: Optional[str] = Field(
        "default",
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
        examples=["[{\"resource_name\": \"myindex\", \"resource_type\": \"INDEX\", \"privileges\": [\"WRITE\"]}]"],
        title="Entity permissions",
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: OpenSearchProviderData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    app: OpenSearchRequirerData
