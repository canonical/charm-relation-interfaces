"""This file defines the schemas for the provider and requirer sides of this relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

import enum
import typing

import pydantic

from interface_tester.schema_base import DataBagSchema


class MimirRole(str, enum.Enum):
    """Mimir component role names."""
    overrides_exporter = "overrides-exporter"
    query_scheduler = "query-scheduler"
    flusher = "flusher"
    query_frontend = "query-frontend"
    querier = "querier"
    store_gateway = "store-gateway"
    ingester = "ingester"
    distributor = "distributor"
    ruler = "ruler"
    alertmanager = "alertmanager"
    compactor = "compactor"

    # meta-roles
    read = "read"
    write = "write"
    backend = "backend"
    all = "all"


class Scheme(str, enum.Enum):
    """Scheme strings."""
    http = "http"
    https = "https"


class MimirClusterProviderAppData(pydantic.BaseModel):
    mimir_config: typing.Dict[str, typing.Any]


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""
    app: MimirClusterProviderAppData


class JujuTopology(pydantic.BaseModel):
    unit: str
    app: str
    charm: str
    model: str
    # in pydantic v2, `model_` is a protected namespace
    juju_model_uuid: str = pydantic.Field(description="Juju model UUID.", alias="model_uuid")


class MimirClusterRequirerUnitData(pydantic.BaseModel):
    juju_topology: JujuTopology
    address: str
    port: int
    scheme: Scheme


class MimirClusterRequirerAppData(pydantic.BaseModel):
    roles: typing.List[MimirRole]


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""
    unit: MimirClusterRequirerUnitData
    app: MimirClusterRequirerAppData
