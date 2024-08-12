"""This file defines the schemas for the provider and requirer sides of the `sdcore_config` relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {
            "webui_url": "sdcore-webui-k8s:9876",
        }
    RequirerSchema:
        unit: <empty>
        app:  <empty>
"""

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field


class SdcoreConfigProviderAppData(BaseModel):
    webui_url: str = Field(
        description="GRPC address of the Webui including Webui hostname and a fixed GRPC port.",
        examples=["sdcore-webui-k8s:9876"]
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of the sdcore_config interface."""
    app: SdcoreConfigProviderAppData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of the sdcore_config interface."""
