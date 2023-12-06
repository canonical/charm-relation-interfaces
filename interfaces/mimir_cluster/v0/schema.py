"""This file defines the schemas for the provider and requirer sides of this relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""
from enum import Enum
from typing import List, Dict, Any

import pydantic
from interface_tester import DataBagSchema


class MimirRole(str, Enum):
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


class MimirClusterProviderAppData(pydantic.BaseModel):
    mimir_config: Dict[str, Any]


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""
    app: MimirClusterProviderAppData


class JujuTopology(pydantic.BaseModel):
    model: str
    unit: str
    # ...


class MimirClusterRequirerUnitData(pydantic.BaseModel):
    juju_topology: JujuTopology
    address: str


class MimirClusterRequirerAppData(pydantic.BaseModel):
    roles: List[MimirRole]


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""
    unit: MimirClusterRequirerUnitData
    app: MimirClusterRequirerAppData