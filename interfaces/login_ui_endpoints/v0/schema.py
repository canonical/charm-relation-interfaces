# Copyright 2023 Canonical
# See LICENSE file for licensing details.
"""This file defines the schemas for the provider and requirer sides of the login_ui_endpoints interface.
It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
Examples:
    ProviderSchema:
        unit: <empty>
        app: {"consent_url": "http://identity-platform-login-ui-url/consent",
              "error_url": "http://identity-platform-login-ui-url/error",
              "index_url": "http://identity-platform-login-ui-url/index",
              "login_url": "http://identity-platform-login-ui-url/login",
              "oidc_error_url": "http://identity-platform-login-ui-url/oidc_error",
              "registration_url": "http://identity-platform-login-ui-url/registration",
              "default_url": "http://identity-platform-login-ui-url"
              }
"""

from pydantic import BaseModel, Field

from interface_tester.schema_base import DataBagSchema


class MyProviderAppData(BaseModel):
    consent_url: str = Field(
        description="Endpoint Hydra forwards users for consent related operations."
    )
    error_url: str = Field(
        description="Endpoint Kratos forwards users to fetch full error messages."
    )
    index_url: str = Field(
        description="Endpoint Kratos forwards users to access index page of Public Login UI."
    )
    login_url: str = Field(
        description="Endpoint Hydra forwards users signing in."
    )
    oidc_error_url: str = Field(
        description="Endpoint Hydra forwards users to access error operations related to OpenID Connect."
    )
    registration_url: str = Field(
        description="Endpoint Kratos forwards users to register."
    )
    default_url: str = Field(
        description="Default Browser endpoint Kratos forwards users to."
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for login_ui_endpoints."""
    app: MyProviderAppData


class RequirerSchema(DataBagSchema):
    """Requirer schema for login_ui_endpoints."""
