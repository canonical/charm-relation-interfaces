"""This file defines the schemas for the provider and requirer sides of the `fiveg_rfsim` interface.
It exposes two interface_tester.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
Examples:
    ProviderSchema:
        unit: <empty>
        app: {
            "version": 0,
            "rfsim_address": "192.168.70.130",
            "sst": 1,
            "sd": 1,
            "band": 77,
            "dl_freq": 4059090000,
            "carrier_bandwidth": 106,
            "numerology": 1,
            "start_subcarrier": 541,
        }
    RequirerSchema:
        unit: <empty>
        app: {
            "version": 0,
        }
"""
from typing import Optional

from pydantic import BaseModel, Field

from interface_tester.schema_base import DataBagSchema


class FivegRFSIMProviderAppData(BaseModel):
    version: int = Field(
        description="Interface version",
        examples=[0, 1, 2, 3],
        ge=0,
    )
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
    band: int = Field(
        description="Frequency band",
        default=None,
        examples=[34, 77, 102],
    )
    dl_freq: int = Field(
        description="Downlink frequency in Hz",
        default=None,
        examples=[4059090000],
    )
    carrier_bandwidth: int = Field(
        description="Carrier bandwidth (number of downlink PRBs)",
        default=None,
        examples=[106],
    )
    numerology: int = Field(
        description="Numerology",
        default=None,
        examples=[0, 1, 2, 3],
    )
    start_subcarrier: int = Field(
        description="First usable subcarrier",
        default=None,
        examples=[530, 541],
    )


class FivegRFSIMRequirerAppData(BaseModel):
    version: int = Field(
        description="Interface version",
        examples=[0, 1, 2, 3],
        ge=0,
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for the fiveg_rfsim interface."""
    app: FivegRFSIMProviderAppData


class RequirerSchema(DataBagSchema):
    """Requirer schema for the fiveg_rfsim interface."""
    app: FivegRFSIMRequirerAppData
