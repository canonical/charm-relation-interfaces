"""This file defines the schemas for the provider and requirer sides of the `fiveg_n3` interface.
It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
Examples:
    ProviderSchema:
        unit: <empty>
        app: {
            "upf_ip_address": "1.2.3.4"
        }
    RequirerSchema:
        unit: <empty>
        app:  <empty>
"""

from pydantic import BaseModel

from interface_tester.schema_base import DataBagSchema


class FivegN3ProviderAppData(BaseModel):
    upf_ip_address: str


class ProviderSchema(DataBagSchema):
    """Provider schema for fiveg_n3."""
    app: FivegN3ProviderAppData


class RequirerSchema(DataBagSchema):
    """Requirer schema for fiveg_n3."""
