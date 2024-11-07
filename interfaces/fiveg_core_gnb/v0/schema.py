"""This file defines the schemas for the provider and requirer sides of the `fiveg_core_gnb` relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {
            "mcc": "001",
            "mnc": "01",
            "tac": 1,
            "sst": 1,
            "sd": 1,
        }
    RequirerSchema:
        unit: <empty>
        app: {
            "cu_id": "gnb001",
        }
"""

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field


class FivegCoreGnbProviderAppData(BaseModel):
    mcc: str = Field(
        description="Mobile Country Code",
        examples=["001"],
        min_length=3,
        max_length=3,
    )
    mnc: str = Field(
        description="Mobile Network Code",
        examples=["01"],
        min_length=2,
        max_length=3,
    )
    tac: int = Field(
        description="Tracking Area Code",
        examples=[1],
        ge=1,
        le=16777215,
    )
    sst: int = Field(
        description="Slice Service Type",
        examples=[1],
        ge=1,
        le=4,
    )
    sd: int = Field(
        description="Slice Differentiator",
        examples=[1],
        ge=1,
        le=16777215,
    )


class FivegCoreGnbRequirerAppData(BaseModel):
    cu_id: str = Field(
        description="Unique identifier of the CU/gnB.",
        examples=["gnb001"]
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of the fiveg_core_gnb interface."""
    app: FivegCoreGnbProviderAppData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of the fiveg_core_gnb interface."""
    app: FivegCoreGnbRequirerAppData
