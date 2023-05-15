"""This file defines the schemas for the provider and requirer sides of the `fiveg_amf_n2` interface.
It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
Examples:
    ProviderSchema:
        unit: <empty>
        app: {"n2IpAddr": "192.168.251.6"}
    RequirerSchema:
        unit: <empty>
        app:  <empty>
"""

from pydantic import BaseModel, IPvAnyAddress, Field

from interface_tester.schema_base import DataBagSchema


class MyProviderAppData(BaseModel):
    url: IPvAnyAddress = Field(
        description="IP Address to reach the AMF's N2 interface.",
        examples=["192.168.251.6"]
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for fiveg_amf_n2."""
    app: MyProviderAppData


class RequirerSchema(DataBagSchema):
    """Requirer schema for fiveg_amf_n2."""
