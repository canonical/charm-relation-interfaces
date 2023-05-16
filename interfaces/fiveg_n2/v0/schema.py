"""This file defines the schemas for the provider and requirer sides of the `fiveg_n2` interface.
It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
Examples:
    ProviderSchema:
        unit: <empty>
        app: {
            "amf_hostname": "amf",
            "ngapp_port": "38412"
        }
    RequirerSchema:
        unit: <empty>
        app:  <empty>
"""

from pydantic import BaseModel

from interface_tester.schema_base import DataBagSchema


class FivegN2ProviderAppData(BaseModel):
    amf_hostname: str
    port: str

class ProviderSchema(DataBagSchema):
    """Provider schema for fiveg_n2."""
    app: FivegN2ProviderAppData


class RequirerSchema(DataBagSchema):
    """Requirer schema for fiveg_n2."""
