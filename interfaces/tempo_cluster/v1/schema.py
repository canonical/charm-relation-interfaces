"""This file defines the schemas for the provider and requirer sides of this relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from enum import Enum
from typing import Dict, List, Optional

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field, Json


class TempoClusterProviderAppData(BaseModel):
    """TempoClusterProviderAppData."""

    worker_config: Json[str] = Field(
        description="The tempo configuration that the requirer should run with."
        "Yaml-encoded. Must conform to the schema that the presently deployed "
        "workload version supports; for example see: "
        "https://grafana.com/docs/tempo/latest/configuration/#configure-tempo."
    )
    loki_endpoints: Optional[Json[Dict[str, str]]] = Field(
        default=None,
        description="List of loki-push-api endpoints to which the worker node can push any logs it generates.",
    )
    ca_cert: Optional[Json[str]] = Field(
        default=None, description="CA certificate for tls encryption."
    )
    server_cert: Optional[Json[str]] = Field(
        default=None, description="Server certificate for tls encryption."
    )
    s3_tls_ca_cert: Optional[Json[str]] = Field(
        default=None, description="CA certificate for the s3 bucket API."
    )
    privkey_secret_id: Optional[Json[str]] = Field(
        default=None,
        description="ID of a Juju secret that holds the private key used by the coordinator for TLS encryption.",
    )
    remote_write_endpoints: Optional[Json[List[Dict[str, str]]]] = Field(
        default=None,
        description="Endpoints to which the workload (and the worker charm) can push metrics to.",
    )
    charm_tracing_receivers: Optional[Json[Dict[str, str]]] = Field(
        default=None,
        description="Endpoints to which the worker node can push its charm traces to."
        "It is a mapping from protocol names such as `zipkin`, `otlp_grpc`, `otlp_http`.",
    )
    workload_tracing_receivers: Optional[Json[Dict[str, str]]] = Field(
        default=None,
        description="Endpoints to which the worker node can push its workload traces to."
        "It is a mapping from protocol names such as `zipkin`, `otlp_grpc`, `otlp_http`.",
    )
    worker_ports: Optional[Json[List[int]]] = Field(
        default=None,
        description="Ports that the worker should open on its pod.",
    )


class _Topology(BaseModel):
    """JujuTopology as defined by cos-lib."""

    application: str
    charm_name: Optional[str]
    unit: Optional[str]


class TempoClusterRequirerUnitData(BaseModel):
    """TempoClusterRequirerUnitData."""

    juju_topology: Json[_Topology]
    address: Json[str]


class TempoRole(str, Enum):
    """Tempo component role names.

    References:
     arch:
      -> https://grafana.com/docs/tempo/latest/operations/architecture/
     config:
      -> https://grafana.com/docs/tempo/latest/configuration/#server
    """

    ALL = "all"  # default, meta-role. gets remapped to scalable-single-binary by the worker.
    QUERIER = "querier"
    QUERY_FRONTEND = "query-frontend"
    INGESTER = "ingester"
    DISTRIBUTOR = "distributor"
    COMPACTOR = "compactor"
    METRICS_GENERATOR = "metrics-generator"


class TempoClusterRequirerAppData(BaseModel):
    """TempoClusterRequirerAppData."""

    role: Json[TempoRole]


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: TempoClusterProviderAppData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    app: TempoClusterRequirerAppData
    unit: TempoClusterRequirerUnitData
