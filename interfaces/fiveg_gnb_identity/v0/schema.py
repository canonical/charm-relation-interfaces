"""This file defines the schemas for the provider and requirer sides of the `fiveg_gnb_identity` relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {
            "gnb_name": "gnb001",
            "tac": 1
        }
    RequirerSchema:
        unit: <empty>
        app:  <empty>
"""

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field


class FivegGnbIdentityProviderAppData(BaseModel):
    gnb_name: str = Field(
        description="Name of the gnB.",
        examples=["gnb001"]
    )
    tac: int = Field(
        description="Tracking Area Code",
        examples=[1]
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of the fiveg_gnb_identity interface."""
    app: FivegGnbIdentityProviderAppData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of the fiveg_gnb_identity interface."""
