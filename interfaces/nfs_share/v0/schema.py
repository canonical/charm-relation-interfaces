"""This file defines the schemas for the provider and require sides of the nfs-share interface.

It exposes two interfaces.schema_base.DataBagSchema subclasses called:

- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {
                "endpoint": "nfs://127.0.0.1/data"
            }

    RequirerSchema:
        unit: <empty>
        app: {
                "name": "app-name",
                "allowlist": "192.36.21.8/24,10.51.19.0/24",
                "size": "100",
            }
"""

from pydantic import BaseModel

from interface_tester.schema_base import DataBagSchema


class NFSShareProviderAppData(BaseModel):
    endpoint: str


class NFSShareRequirerAppData(BaseModel):
    name: str
    allowlist: str
    size: str


class ProviderSchema(DataBagSchema):
    """Provider schema for nfs-share."""
    app: NFSShareProviderAppData


class RequirerSchema(DataBagSchema):
    """Requirer schema for nfs-share."""
    app: NFSShareRequirerAppData

