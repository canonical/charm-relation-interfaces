"""This file defines the schemas for the provider and requirer sides of the `fiveg_f1` interface.
It exposes two interface_tester.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
Examples:
    ProviderSchema:
        unit: <empty>
        app: {
            "f1_ip_address": "192.168.70.132",
            "f1_port": 2153
        }
    RequirerSchema:
        unit: <empty>
        app:  {
            "f1_port": 2153
        }
"""

from pydantic import BaseModel, IPvAnyAddress, Field

from interface_tester.schema_base import DataBagSchema


class FivegF1ProviderAppData(BaseModel):
    f1_ip_address: IPvAnyAddress = Field(
        description="IPv4 address of the network interface used for F1 traffic",
        examples=["192.168.70.132"]
    )
    f1_port: int = Field(
        description="Number of the port used for F1 traffic",
        examples=[2153]
    )


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
