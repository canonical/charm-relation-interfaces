"""This file defines the schemas for the provider and requirer sides of this relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field


class ProviderAppSchema(BaseModel):
    """Application databag schema for the provider side of the profiling interface."""
    otlp_grpc_endpoint_url:str = Field(
        description="Grpc ingestion endpoint for profiles using otlp_grpc.",
        examples=["some.hostname:1234", "10.64.140.43:42424"]
    )
    otlp_http_endpoint_url:str = Field(
        description="Ingestion endpoint for profiles using any supported format such as pprof, "
                    "folded, lines. Cfr. grafana.com/docs/pyroscope/latest/reference-server-api/ "
                    "for the upstream docs.",
        examples=["http://10.64.140.43/foo-pyroscope/ingest",
                  "https://some.hostname/ingest"]
    )



class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""
    app: ProviderAppSchema

class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""
