"""This file defines the schemas for the provider and requirer sides of the `fiveg_n4` interface.

It exposes two `interfaces.schema_base.DataBagSchema` subclasses called:
- `ProviderSchema`
- `RequirerSchema`

Examples:

    ProviderSchema:
        unit: <empty>
        app: {
            "upf_hostname": "upf.uplane-cloud.canonical.com",
            "upf_port": 8805
        }

    RequirerSchema:
        unit: <empty>
        app:  <empty>
"""

from pydantic import BaseModel, Field

from interface_tester.schema_base import DataBagSchema


class FivegN4ProviderAppData(BaseModel):
    upf_hostname: str = Field(
        description="Name of the host exposing the UPF's N4 interface.",
        examples=["upf.uplane-cloud.canonical.com"]
    )
    upf_port: int = Field(
        description="Port on which UPF's N4 interface is exposed.",
        examples=[8805]
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for fiveg_n4."""
    app: FivegN4ProviderAppData


class RequirerSchema(DataBagSchema):
    """Requirer schema for fiveg_n4."""
