"""This file defines the schemas for the provider and requirer sides of the `fiveg_rfsim` interface.
It exposes two interface_tester.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
Examples:
    ProviderSchema:
        unit: <empty>
        app: {
            "rfsim_address": "192.168.70.130",
            "sst": 1,
            "sd": 1,
        }
    RequirerSchema:
        unit: <empty>
        app:  <empty>
"""
from typing import Optional

from pydantic import BaseModel, Field

from interface_tester.schema_base import DataBagSchema


class FivegRFSIMProviderAppData(BaseModel):
    rfsim_address: str = Field(
        description="RF simulator service ip",
        examples=["192.168.70.130"]
    )
    sst: int = Field(
        description="Slice/Service Type",
        examples=[1, 2, 3, 4],
        ge=0,
        le=255,
    )
    sd: Optional[int] = Field(
        description="Slice Differentiator",
        default=None,
        examples=[1],
        ge=0,
        le=16777215,
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for the fiveg_rfsim interface."""
    app: FivegRFSIMProviderAppData


class RequirerSchema(DataBagSchema):
    """Requirer schema for the fiveg_rfsim interface."""
