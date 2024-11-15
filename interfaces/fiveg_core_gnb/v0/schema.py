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
            "cu_name": "gnb001",
        }
"""

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field
from typing import List


class FivegCoreGnbProviderAppData(BaseModel):
    tac: int = Field(
        description="Tracking Area Code",
        examples=[1],
        ge=1,
        le=16777215,
    )
    plmns: List[dict]


class FivegCoreGnbRequirerAppData(BaseModel):
    cu_name: str = Field(
        description="Unique identifier of the CU/gnB.",
        examples=["gnb001"]
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of the fiveg_core_gnb interface."""
    app: FivegCoreGnbProviderAppData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of the fiveg_core_gnb interface."""
    app: FivegCoreGnbRequirerAppData
