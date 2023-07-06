"""This file defines the schemas for the provider and requirer sides of the kratos_endpoints interface.
It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {"admin_endpoint": "http://kratos-url:4434",
              "public_endpoint": "http://kratos-url:4433",
              "login_browser_endpoint": "http://kratos-url:4433/self-service/login/browser",
              "sessions_endpoint": "http://kratos-url:4433/sessions/whoami"
              }
"""

from pydantic import BaseModel, Field

from interface_tester.schema_base import DataBagSchema


class KratosEndpointsProvider(BaseModel):
    admin_endpoint: str = Field(
        description="Kratos admin URL."
    )
    public_endpoint: str = Field(
        description="Kratos public URL."
    )
    login_browser_endpoint: str = Field(
        description="The Kratos endpoint that initializes a browser-based user login flow."
    )
    sessions_endpoint: str = Field(
        description="The Kratos endpoint to check who the current session belongs to."
    )

class ProviderSchema(DataBagSchema):
    """Provider schema for kratos_endpoints."""
    app: KratosEndpointsProvider


class RequirerSchema(DataBagSchema):
    """Requirer schema for kratos_endpoints."""
