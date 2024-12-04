"""This file defines the schemas for the provider and requirer sides of the `fiveg_core_gnb` relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {
            "tac": 1,
            "plmns": [
                {
                    "mcc": "001",
                    "mnc": "01",
                    "sst": 1,
                    "sd": 1,
                }
            ],
        }
    RequirerSchema:
        unit: <empty>
        app: {
            "gnb-name": "gnb001",
        }
"""

from dataclasses import dataclass
from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field
from typing import List, Optional


@dataclass
class PLMNConfig:
    """Dataclass representing the configuration for a PLMN."""

    mcc: str = Field(
        description="Mobile Country Code",
        examples=["001", "208", "302"],
        pattern=r"^[0-9][0-9][0-9]$",
    )
    mnc: str = Field(
        description="Mobile Network Code",
        examples=["01", "001", "999"],
        pattern=r"^[0-9][0-9][0-9]?$",
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


class FivegCoreGnbProviderAppData(BaseModel):
    tac: int = Field(
        description="Tracking Area Code",
        examples=[1],
        ge=1,
        le=16777215,
    )
    plmns: List[PLMNConfig]


class FivegCoreGnbRequirerAppData(BaseModel):
    gnb_name: str = Field(
        alias="gnb-name",
        description="Unique identifier of the CU/gnB.",
        examples=["gnb001"]
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of the fiveg_core_gnb interface."""
    app: FivegCoreGnbProviderAppData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of the fiveg_core_gnb interface."""
    app: FivegCoreGnbRequirerAppData
