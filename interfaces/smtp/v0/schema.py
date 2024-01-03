# Copyright 2023 Canonical
# See LICENSE file for licensing details.
"""This file defines the schema for the provider side of the smtp interface.

It exposes one interfaces.schema_base.DataBagSchema subclass called:
- ProviderSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {"smtp":
                 {
                    "host": "example.com",
                    "port": "587",
                    "user": "example_user",
                    "password_id": "secret:123213123123123123123",
                    "auth_type": "plain",
                    "transport_security": "tls",
                    "domain": "example.com",
                }
             }
"""
from enum import Enum
from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field
from typing import Optional


class TransportSecurity(str, Enum):
    """Represent the transport security values."""

    NONE = "none"
    STARTTLS = "starttls"
    TLS = "tls"


class AuthType(str, Enum):
    """Represent the auth type values."""

    NONE = "none"
    NOT_PROVIDED = "not_provided"
    PLAIN = "plain"


class SmtpProviderData(BaseModel):
    host: str = Field(
        min_length=1,
        description="SMTP host.",
        title="Host",
        examples=["example.com"],
    )
    port: int = Field(
        ge=1,
        le=65536,
        description="SMTP port.",
        title="Port",
        examples=[25, 587, 465],
    )
    user: Optional[str] = Field(
        description="SMTP user.",
        title="User",
        examples=["some_user"],
    )
    password: Optional[str] = Field(
        description="SMTP password. Populated instead of password_id when secrets are not supported.",
        title="Password",
        examples=["somepasswd"],
    )
    password_id: Optional[str] = Field(
        description="Juju secret ID for the SMTP password. Populated instead of password when secrets are supported.",
        title="Password ID",
        examples=["secret:123213123123123123123"],
    )
    auth_type: AuthType = Field(
        description="The type used to authenticate with the SMTP relay.",
        title="Auth type",
        examples=[AuthType.NONE],
    )
    transport_security: TransportSecurity = Field(
        description="The security protocol to use for the SMTP relay.",
        title="Transport security",
        examples=[TransportSecurity.NONE],
    )
    domain: Optional[str] = Field(
        description="The MAIL FROM domain for the outgoing email.",
        title="Domain",
        examples=["example.com"],
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for SMTP."""

    app: SmtpProviderData


class RequirerSchema(DataBagSchema):
    """Requirer schema for SMTP."""
