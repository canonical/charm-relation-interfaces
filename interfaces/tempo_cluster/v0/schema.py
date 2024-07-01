"""This file defines the schemas for the provider and requirer sides of this relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""
from enum import Enum
from typing import Optional, Dict, Any, Literal

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel

ReceiverProtocol = Literal[
    "zipkin",
    "otlp_grpc",
    "otlp_http",
]

class TempoClusterProviderAppData(BaseModel):
    """TempoClusterProviderAppData."""
    tempo_config: Dict[str, Any]
    loki_endpoints: Optional[Dict[str, str]] = None
    ca_cert: Optional[str] = None
    server_cert: Optional[str] = None
    privkey_secret_id: Optional[str] = None
    tempo_receiver: Optional[Dict[ReceiverProtocol, str]] = None


class JujuTopology(BaseModel):
    """JujuTopology as defined by cos-lib."""
    model: str
    model_uuid: str
    application: str
    charm_name: str
    unit: str


class TempoClusterRequirerUnitData(BaseModel):
    """TempoClusterRequirerUnitData."""

    juju_topology: JujuTopology
    address: str


class TempoRole(str, Enum):
    """Tempo component role names.

    References:
     arch:
      -> https://grafana.com/docs/tempo/latest/operations/architecture/
     config:
      -> https://grafana.com/docs/tempo/latest/configuration/#server
    """
    all = "all"  # default, meta-role. gets remapped to scalable-single-binary by the worker.

    querier = "querier"
    query_frontend = "query-frontend"
    ingester = "ingester"
    distributor = "distributor"
    compactor = "compactor"
    metrics_generator = "metrics-generator"


class TempoClusterRequirerAppData(BaseModel):
    """TempoClusterRequirerAppData."""

    role: TempoRole


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""
    app: TempoClusterProviderAppData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""
    app: TempoClusterRequirerAppData
    unit: TempoClusterRequirerUnitData
