# Copyright 2024 Canonical
# See LICENSE file for licensing details.
"""This file defines the schemas for the provider and requirer sides of the tracing interface.

It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    RequirerSchema:
        unit_data: <empty>
        application_data:
          receivers:
            - otlp_grpc
            - otlp_http

    ProviderSchema:
        # unit_data: <empty>
        application_data:            
          receivers:
            - protocol: 
                name: otlp_http
                type: http
              url: http://traefik_address:2331
            - protocol: 
                name: otlp_grpc
                type: grpc
              url: traefik_address:2331

"""
from typing import List
import enum

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Json, Field, ConfigDict


class TransportProtocolType(str, enum.Enum):
    """Receiver Type."""

    http = "http"
    grpc = "grpc"


class ProtocolType(BaseModel):
    """Protocol Type."""

    model_config = ConfigDict(
        # Allow serializing enum values.
        use_enum_values=True
    )
    """Pydantic config."""

    name: str = Field(
        ...,
        description="Receiver protocol name. What protocols are supported (and what they are called) "
        "may differ per provider.",
        examples=["otlp_grpc", "otlp_http", "tempo_http", "jaeger_thrift_compact"],
    )
    type: TransportProtocolType = Field(
        ...,
        description="The transport protocol used by this receiver.",
        examples=["http", "grpc"],
    )


class Receiver(BaseModel):
    """Specification of an active receiver."""

    protocol: ProtocolType = Field(..., description="Receiver protocol name and type.")
    url: str = Field(
        ...,
        description="""URL at which the receiver is reachable. If there's an ingress, it would be the external URL.
        Otherwise, it would be the service's fqdn or internal IP.
        If the protocol type is grpc, the url will not contain a scheme.""",
        examples=[
            "http://traefik_address:2331",
            "https://traefik_address:2331",
            "http://tempo_public_ip:2331",
            "https://tempo_public_ip:2331",
            "tempo_public_ip:2331",
        ],
    )


class TracingProviderData(BaseModel):
    receivers: Json[List[Receiver]] = Field(
        ...,
        description="A list of enabled receivers in the form of the protocol they use and their resolvable server url.",
    )


class TracingRequirerData(BaseModel):
    receivers: Json[List[str]] = Field(
        ..., description="List of protocols that the requirer wishes to use."
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for Tracing."""

    app: TracingProviderData


class RequirerSchema(DataBagSchema):
    """Requirer schema for Tracing."""

    app: TracingRequirerData
