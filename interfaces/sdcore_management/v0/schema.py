"""This file defines the schemas for the provider and requirer sides of the `sdcore_management` relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {
            "management_endpoint": "http://1.2.3.4:1234",
        }
    RequirerSchema:
        unit: <empty>
        app:  <empty>
"""

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field, HttpUrl


class SdcoreManagementProviderAppData(BaseModel):
    management_url: HttpUrl = Field(
        description="The endpoint to use to manage SD-Core network.",
        examples=["http://1.2.3.4:1234"],
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of the sdcore_management interface."""

    app: SdcoreManagementProviderAppData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of the sdcore_management interface."""
