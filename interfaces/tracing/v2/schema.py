# Copyright 2024 Canonical
# See LICENSE file for licensing details.
"""This file defines the schemas for the provider and requirer sides of the tracing interface.

It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        unit_data: <empty>
        application_data:
          receivers:
            - otlp_grpc
            - otlp_http

    RequirerSchema:
        # unit_data: <empty>
        application_data:
          url: "http://foo.bar/my-model-my-unit-0"
          receivers:
            - type: otlp_grpc
              port: 1234
            - type: otlp_http
              port: 5678
"""
from typing import List, Optional

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Json, Field


class Receiver(BaseModel):
    """Specification of an active receiver."""
    port: int = Field(...,
                      description="Port at which the receiver is listening.",
                      examples=[42, 9098])
    protocol: str = Field(
        ...,
        description="Receiver protocol name. What protocols are supported (and what they are called) "
                    "may differ per provider.",
        examples=["otlp_grpc", "otlp_http", "tempo_http", "jaeger_thrift_compact"])


class TracingProviderData(BaseModel):
    host: str = Field(..., description="Hostname of the tracing server.", examples=["example.com"])
    receivers: Json[List[Receiver]] = Field(
        ...,
        description="List of the receivers that this server has enabled, and their ports.")


class ProviderSchema(DataBagSchema):
    """Provider schema for Tracing."""
    app: TracingProviderData


class RequirerSchema(DataBagSchema):
    """Requirer schema for Tracing."""
    protocols: Json[List[str]] = Field(
        ...,
        description="List of protocols that the requirer wishes to use."
    )
