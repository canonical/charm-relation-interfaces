"""This file defines the schemas for the provider and requirer sides of the auth_proxy interface.
It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    RequirerSchema:
        unit: <empty>
        app: {
          "providers": [
            "protected_urls": ["https://example.com", "https://other-example.com"],
            "allowed_endpoints": ["about/app", "welcome"],
            "headers": ["X-User", "X-Some-Header"]
          ]
        }

    ProviderSchema:
        unit: <empty>
        app: <empty>
"""

from typing import List, Optional
from pydantic import AnyHttpUrl, BaseModel, Field

from interface_tester.schema_base import DataBagSchema


class AuthProxyRequirer(BaseModel):
    protected_urls: List[AnyHttpUrl] = Field(
        description="List of urls to be protected by Identity and Access Proxy."
    )
    allowed_endpoints: Optional[List[str]] = Field(
        description="List of endpoints that are allowed to bypass authentication."
    )
    headers: Optional[List[str]] = Field(
        description="List of headers to be returned upon a successful authentication."
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for auth_proxy."""


class RequirerSchema(DataBagSchema):
    """Requirer schema for auth_proxy."""
    app: AuthProxyRequirer
