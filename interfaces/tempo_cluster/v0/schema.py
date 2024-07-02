"""This file defines the schemas for the provider and requirer sides of this relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""
from enum import Enum
from typing import Optional, Dict, Any, Literal

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field


class TempoClusterProviderAppData(BaseModel):
    """TempoClusterProviderAppData."""
    tempo_config: str = Field(
        description="The tempo configuration that the requirer should run with."
                    "Yaml-encoded. Conform the schema that the workload version supports; "
                    "for example see: "
                    "https://grafana.com/docs/tempo/latest/configuration/#configure-tempo."
    )
    loki_endpoints: Optional[Dict[str, str]] = Field(
        default=None,
        description="List of loki-push-api endpoints to which the worker node can push any logs it generates.")
    ca_cert: Optional[str] = Field(default=None, description="CA certificate for tls encryption.")
    server_cert: Optional[str] = Field(default=None, description="Server certificate for tls encryption.")
    privkey_secret_id: Optional[str] = Field(
        default=None,
        description="Private key used by the coordinator, for tls encryption."
    )
    tempo_receiver: Optional[Dict[str, str]] = Field(
        default=None,
        description="Tempo receiver protocols to which the worker node can push any traces it generates."
                    "It is a mapping from protocol names such as `zipkin`, `otlp_grpc`, `otlp_http`."
                    "The actual protocol names depend on what the Tempo version that the "
                    "applications are operating currently support. See the `tracing` interface "
                    "specification for more information on this."
    )


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
