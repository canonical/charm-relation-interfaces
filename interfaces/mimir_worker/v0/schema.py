"""This file defines the schemas for the provider and requirer sides of this relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""
from enum import Enum
from typing import Dict, List

import pydantic
from pydantic import Json

from interfaces.schema_base import DataBagSchema


class MimirRole(str, Enum):
    """Mimir component role names."""
    overrides_exporter = "overrides_exporter"
    query_scheduler = "query_scheduler"
    flusher = "flusher"
    query_frontend = "query_frontend"
    querier = "querier"
    store_gateway = "store_gateway"
    ingester = "ingester"
    distributor = "distributor"
    ruler = "ruler"
    alertmanager = "alertmanager"
    compactor = "compactor"


class S3Config(pydantic.BaseModel):
    url: str
    endpoint: str
    secret_key: str
    access_key: str
    insecure: bool


class MyProviderAppDataBag(pydantic.BaseModel):
    hash_ring: Json[List[str]]
    s3_config: Json[S3Config]
    config: Json[Dict[str, str]]


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""
    app: MyProviderAppDataBag


class JujuTopology(pydantic.BaseModel):
    model: str
    unit: str
    # ...


class MyRequirerUnitDataBag(pydantic.BaseModel):
    juju_topology: Json[JujuTopology]  # todo [Luca]: change to whatever 'find this unit' info we need, e.g. an address


class MyRequirerAppDataBag(pydantic.BaseModel):
    roles: List[MimirRole]


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""
    unit: MyRequirerUnitDataBag
    app: MyRequirerAppDataBag
