# Copyright 2023 Canonical
# See LICENSE file for licensing details.
"""This file defines the schemas for the provider and requirer sides of the tracing interface.

It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        unit_data: <empty>
        application_data: <empty>

    RequirerSchema:
        # unit_data: <empty>
        application_data:
          url: "http://foo.bar/my-model-my-unit-0"
          ingester-ports:
            - type: otlp_grpc
              port: 1234
            - type: otlp_http
              port: 5678
"""
from enum import Enum
from typing import List, Literal

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Json


class IngesterProtocol(str, Enum):
    jaeger_grpc = "jaeger_grpc"
    jaeger_http_thrift = "jaeger_http_thrift"
    otlp_grpc = "otlp_grpc"
    otlp_http = "otlp_http"
    zipkin = "zipkin"
    tempo = "tempo"


class Ingester(BaseModel):
    port: int
    protocol: IngesterProtocol


class TracingProviderData(BaseModel):
    host: str
    ingesters: Json[List[Ingester]]


class ProviderSchema(DataBagSchema):
    """Provider schema for Tracing."""
    app: TracingProviderData


class RequirerSchema(DataBagSchema):
    """Requirer schema for Tracing."""
