# Copyright 2023 Canonical
# See LICENSE file for licensing details.
"""This file defines the schemas for the provider and requirer sides of the tracing interface.

It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: <empty>

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
from typing import List, Literal

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Json

IngesterProtocol = Literal['otlp_grpc', 'otlp_http', 'zipkin', 'tempo']


class Ingester(BaseModel):
    port: str
    protocol: str


class TracingRequirerData(BaseModel):
    url: str
    ingesters: Json[List[Ingester]]


class RequirerSchema(DataBagSchema):
    """Requirer schema for Tracing."""
    app: TracingRequirerData


class ProviderSchema(DataBagSchema):
    """Provider schema for Tracing."""
