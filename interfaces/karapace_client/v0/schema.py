"""This file defines the schemas for the provider and requirer sides of the karapace_client interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from enum import Enum
from typing import Optional

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field, field_validator


class ExtraUserRole(str, Enum):
    admin = "admin"
    user = "user"


class KarapaceProviderData(BaseModel):
    """The databag for the provider side of this interface."""

    subject: str = Field(
        description="The subject that has been made available to the relation user. Name defined in the Requirer's subject field",
        examples=["subject-1"],
        title="Subject name",
    )

    username: str = Field(
        description="Username for connecting to the Karapace service",
        examples=["relation-14"],
        title="Karapace username",
    )

    password: str = Field(
        description="Password for connecting to the Karapace service",
        examples=["alphanum-32byte-random"],
        title="Karapace password",
    )

    endpoints: str = Field(
        description="A list of endpoints used to connect to the subject",
        examples=["10.141.78.155:8082,10.141.78.62:8082,10.141.78.186:8082"],
        title="Karapace server endpoints",
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


class KarapaceRequirerData(BaseModel):
    """The databag for the requirer side of this interface."""

    subject: str = Field(
        description="The subject name access requested by the requirer",
        examples=["subject-1"],
        title="Subject name",
    )

    extra_user_roles: Optional[str] = Field(
        default="admin",
        alias="extra-user-roles",
        description="Any extra user roles requested by the requirer",
        examples=["admin", "user"],
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
        examples=["[{\"resource_name\": \"schemas\", \"resource_type\": \"SUBJECT\", \"privileges\": [\"READ\"]}]"],
        title="Entity permissions",
    )

    @field_validator("extra_user_roles", mode="before")
    @classmethod
    def extra_user_roles_validator(cls, value: str) -> str:
        try:
            _role = ExtraUserRole(value)
        except ValueError:
            raise ValueError(f"Role {value} is not valid.")

        return value


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: KarapaceProviderData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    app: KarapaceRequirerData
