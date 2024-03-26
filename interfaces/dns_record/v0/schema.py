# Copyright 2023 Canonical
# See LICENSE file for licensing details.
"""This file defines the schemas for the provider and requirer sides of the dns_record interface.
It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    RequirerSchema:
        unit: <empty>
        app: {
          "dns-domains": [
            {
              "domain": "cloud.canonical.com",
              "username": "user1",
              "password": "secret:123213123123123123123"
            },
            {
              "domain": "staging.ubuntu.com",
              "username": "user2",
              "password": "secret:123213123123123123123"
            }
          ]
        }

    ProviderSchema:
        unit: <empty>
        app: {
          "dns-domains": [
            {
              "domain": "cloud.canonical.com",
              "status": "denied",
              "status_description": "incorrect username and password"
            },
            {
              "domain": "staging.ubuntu.com",
              "status": "approved"
            }
          ]
        }
"""

from enum import Enum
from typing import List, Optional
from pydantic import AnyHttpUrl, BaseModel, Field

from interface_tester.schema_base import DataBagSchema


class Status(str, Enum):
    """Represent the status values."""

    APPROVED = "approved"
    DENIED = "denied"


class ProviderDomains:
    domain: str = Field(
        min_length=1,
        name="Domain",
        description="Domain name requested.",
        examples=["cloud.canonical.com", "staging.ubuntu.com"]
    )
    status: Status = Field(
        name="Status",
        description="Status for the domain request.",
        examples=[Status.APPROVED, Status.DENIED]
    )
    status_description: Optional[str] = Field(
        name="Status description",
        description="Status description.",
        examples=["incorrect username and password"]
    )


class DnsRecordProvider(BaseModel):
    """List statuses for the DNS records informed by the requirer."""
    dns_domains: List[ProviderDomains] = Field(
        description="List statuses for the DNS records informed by the requirer."
    )


class RequirerDomains:
    domain: str = Field(
        min_length=1,
        name="Domain",
        description="Domain name for the provider to manage.",
        examples=["cloud.canonical.com", "staging.ubuntu.com"]
    )
    username: str = Field(
        name="Username",
        description="Username for authentication.",
        examples=["user1", "user2"],
    )
    password: str = Field(
        name="Password",
        description="Juju secret containing the user password.",
        examples=["secret:123213123123123123123"],
    )


class DnsRecordRequirer(BaseModel):
    """List of domains for the provider to manage."""
    dns_domains: List[RequirerDomains] = Field(
        description="List of DNS records for the provider to manage."
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for dns_record."""
    app: DnsRecordProvider


class RequirerSchema(DataBagSchema):
    """Requirer schema for dns_record."""
    app: DnsRecordRequirer
