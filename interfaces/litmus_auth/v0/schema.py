"""This file defines the schemas for the provider and requirer sides of this relation interface.
It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field


class AppSchema(BaseModel):
    """Application databag schema for the provider & requrier side of the litmus_auth interface."""

    grpc_server_host: str = Field(
        description="gRPC server hostname for the litmus auth/backend server.",
        examples=["some.hostname", "10.64.140.43"],
    )
    grpc_server_port: int = Field(
        description="gRPC server port for the litmus auth/backend server.",
        examples=[1234, 42424],
    )
    insecure: bool = Field(
        description="Whether the gRPC server endpoint should be accessed without TLS (insecure connection).",
        default=False,
    )
    version: int = Field(
        description="version of this data model.",
        default=0,
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: AppSchema


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    app: AppSchema
