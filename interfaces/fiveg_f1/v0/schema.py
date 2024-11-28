"""This file defines the schemas for the provider and requirer sides of the `fiveg_f1` interface.
It exposes two interface_tester.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
Examples:
    ProviderSchema:
        unit: <empty>
        app: {
            "f1_ip_address": "192.168.70.132",
            "f1_port": 2153,
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
        app:  {
            "f1_port": 2153
        }
"""

from pydantic import BaseModel, IPvAnyAddress, Field
from dataclasses import dataclass
from interface_tester.schema_base import DataBagSchema
from typing import List, Optional, conlist

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

class FivegF1ProviderAppData(BaseModel):
    f1_ip_address: IPvAnyAddress = Field(
        description="IPv4 address of the network interface used for F1 traffic",
        examples=["192.168.70.132"]
    )
    f1_port: int = Field(
        description="Number of the port used for F1 traffic",
        examples=[2153]
    )
    tac: int = Field(
        description="Tracking Area Code",
        examples=[1],
        ge=1,
        le=16777215,
    )
    plmns: conlist(PLMNConfig, min_length=1)


class FivegF1RequirerAppData(BaseModel):
    f1_port: int = Field(
        description="Number of the port used for F1 traffic",
        examples=[2153]
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for fiveg_f1."""
    app: FivegF1ProviderAppData


class RequirerSchema(DataBagSchema):
    """Requirer schema for fiveg_f1."""
    app: FivegF1RequirerAppData
