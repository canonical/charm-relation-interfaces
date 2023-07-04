"""This file defines the schemas for the provider and requirer sides of the `fiveg_n2` interface.
It exposes two interface_tester.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
Examples:
    ProviderSchema:
        unit: <empty>
        app: {
            "amf_ip_address": "192.168.70.132",
            "amf_hostname": "amf",
            "amf_port": 38412
        }
    RequirerSchema:
        unit: <empty>
        app:  <empty>
"""

from pydantic import BaseModel, IPvAnyAddress, Field

from interface_tester.schema_base import DataBagSchema


class FivegN2ProviderAppData(BaseModel):
    amf_ip_address: IPvAnyAddress = Field(
        description="IP Address to reach the AMF's N2 interface.",
        examples=["192.168.70.132"]
    )
    amf_hostname: str = Field(
        description="Hostname to reach the AMF's N2 interface.",
        examples=["amf"]
    )
    amf_port: int = Field(
        description="Port to reach the AMF's N2 interface.",
        examples=[38412]
    )

class ProviderSchema(DataBagSchema):
    """Provider schema for fiveg_n2."""
    app: FivegN2ProviderAppData


class RequirerSchema(DataBagSchema):
    """Requirer schema for fiveg_n2."""
