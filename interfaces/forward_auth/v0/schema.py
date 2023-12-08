"""This file defines the schemas for the provider and requirer sides of the forward_auth interface.
It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {
            "decisions_address": "https://oathkeeper-0.oathkeeper-endpoints.namespace.svc.cluster.local:4456/decisions",
            "app_names": ["charmed-app", "other-charmed-app"],
            "headers": ["X-User", "X-Some-Header"]
        }

    RequirerSchema:
        unit: <empty>
        app: {
            "ingress_app_names": ["charmed-app", "other-charmed-app"]
        }
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from interface_tester.schema_base import DataBagSchema


class ForwardAuthProvider(BaseModel):
    decisions_address: str = Field(
        description="The internal decisions endpoint address."
    )
    app_names: List[str] = Field(
        description="List of names of applications requesting to be protected by Identity and Access Proxy."
    )
    headers: Optional[List[str]] = Field(
        description="List of headers to copy from the authentication server response and set on forwarded requests."
    )


class ForwardAuthRequirer(BaseModel):
    ingress_app_names: Optional[List[str]] = Field(
        description="List of names of applications that are related via ingress."
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for forward_auth."""
    app: ForwardAuthProvider


class RequirerSchema(DataBagSchema):
    """Requirer schema for forward_auth."""
    app: ForwardAuthRequirer
