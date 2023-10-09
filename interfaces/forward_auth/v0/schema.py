"""This file defines the schemas for the provider and requirer sides of the forward_auth interface.
It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    RequirerSchema:
        unit: <empty>
        app: {
          "providers": [
            "decisions_address": "http://oathkeeper-0.oathkeeper-endpoints.namespace.svc.cluster.local:4456/decisions",
            "app_names": ["charmed-app", "other-charmed-app"],
            "headers": ["X-User", "X-Some-Header"]
          ]
        }

    ProviderSchema:
        unit: <empty>
        app: <empty>
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from interface_tester.schema_base import DataBagSchema


class ForwardAuthRequirer(BaseModel):
    decisions_address: str = Field(
        description="The internal decisions endpoint address."
    )
    app_names: List[str] = Field(
        description="List of names of applications requesting to be protected by Identity and Access Proxy."
    )
    headers: Optional[List[str]] = Field(
        description="List of headers to copy from the authentication server response and set on forwarded requests."
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for forward_auth."""


class RequirerSchema(DataBagSchema):
    """Requirer schema for forward_auth."""
    app: ForwardAuthRequirer
