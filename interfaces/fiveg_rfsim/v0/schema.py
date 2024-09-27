"""This file defines the schemas for the provider and requirer sides of the `fiveg_rfsim` interface.
It exposes two interface_tester.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
Examples:
    ProviderSchema:
        unit: <empty>
        app: {
            "rfsim_address": "192.168.70.130",
        }
    RequirerSchema:
        unit: <empty>
        app:  <empty>
"""

from pydantic import BaseModel, Field

from interface_tester.schema_base import DataBagSchema


class FivegRFSIMProviderAppData(BaseModel):
    rfsim_address: str = Field(
        description="RF simulator service address which is equal to DU pod ip",
        examples=["192.168.70.130"]
    )

class ProviderSchema(DataBagSchema):
    """Provider schema for the fiveg_rfsim interface."""
    app: FivegRFSIMProviderAppData


class RequirerSchema(DataBagSchema):
    """Requirer schema for the fiveg_rfsim interface."""