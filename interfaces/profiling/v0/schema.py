"""This file defines the schemas for the provider and requirer sides of this relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field


class ProviderAppSchema(BaseModel):
    """Application databag schema for the provider side of the profiling interface."""

    otlp_grpc_endpoint_url: str = Field(
        description="Grpc ingestion endpoint for profiles using otlp_grpc.",
        examples=["some.hostname:1234", "10.64.140.43:42424"],
    )
    insecure: bool = Field(
        description="Whether the ingestion endpoints should be accessed without TLS (insecure connection).",
        default=False,
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: ProviderAppSchema


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""
