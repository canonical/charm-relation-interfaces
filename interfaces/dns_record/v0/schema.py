# Copyright 2024 Canonical
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
              "uuid": "550e8400-e29b-41d4-a716-446655440000",
              "domain": "cloud.canonical.com",
              "username": "user1",
              "password": "secret:123213123123123123123"
            },
            {
              "uuid": "550e8400-e29b-41d4-a716-446655440001",
              "domain": "staging.ubuntu.com",
              "username": "user2",
              "password": "secret:123213123123123123123"
            }
          ],
          "dns-entries": [
            {
              "uuid": "550e8400-e29b-41d4-a716-446655440002",
              "domain": "cloud.canonical.com",
              "host_label": "admin",
              "ttl": 600,
              "record_class": "IN",
              "record_type": "A",
              "record_data": "91.189.91.48"
            },
            {
              "uuid": "550e8400-e29b-41d4-a716-446655440003",
              "domain": "staging.canonical.com",
              "host_label": "www",
              "record_data": "91.189.91.47"
            }
          ]
        }

    ProviderSchema:
        unit: <empty>
        app: {
          "dns-domains": [
            {
              "uuid": "550e8400-e29b-41d4-a716-446655440000",
              "status": "failure",
              "description": "incorrect username and password"
            },
            {
              "uuid": "550e8400-e29b-41d4-a716-446655440001",
              "status": "approved"
            }
          ],
          "dns-entries": [
            {
              "uuid": "550e8400-e29b-41d4-a716-446655440002",
              "status": "failure",
              "description": "incorrect username & password"
            },
            {
              "uuid": "550e8400-e29b-41d4-a716-446655440003",
              "status": "approved"
            }
        ]

        }
"""

from enum import Enum
from typing import List
from pydantic import IPvAnyAddress, BaseModel, Field

from interface_tester.schema_base import DataBagSchema


class Status(str, Enum):
    """Represent the status values."""

    APPROVED = "approved"
    INVALID_CREDENTIALS = "invalid_credentials"
    PERMISSION_DENIED = "permission_denied"
    CONFLICT = "conflict"
    INVALID_DATA = "invalid_data"
    FAILURE = "failure"
    PENDING = "pending"


class RecordType(str, Enum):
    """Represent the DNS record types."""

    A = "A"
    AAAA = "AAAA"
    CNAME = "CNAME"
    MX = "MX"
    DKIM = "DKIM"
    SPF = "SPF"
    DMARC = "DMARC"
    TXT = "TXT"
    CAA = "CAA"
    SRV = "SRV"
    SVCB = "SVCB"
    HTTPS = "HTTPS"
    PTR = "PTR"
    SOA = "SOA"
    NS = "NS"
    DS = "DS"
    DNSKEY = "DNSKEY"


class RecordClass(str, Enum):
    """Represent the DNS record classes."""

    IN = "IN"


class DnsProviderData(BaseModel):
    uuid: str = Field(
        min_length=1,
        name="UUID",
        description="UUID for this domain as specified by the requirer.",
        examples="550e8400-e29b-41d4-a716-446655440000"
    )
    status: Status = Field(
        name="Status",
        description="Status for the domain request.",
        examples=[Status.APPROVED, Status.INVALID_CREDENTIALS]
    )
    description: str = Field(
        default=None,
        name="Status description",
        description="Status description.",
        examples=["incorrect username and password"]
    )


class DNSRecordProvider(BaseModel):
    """List statuses for the DNS records informed by the requirer."""
    dns_domains: List[DnsProviderData] = Field(
        default=None,
        description="List statuses for the domains requested by the requirer."
    )
    dns_entries: List[DnsProviderData] = Field(
        default=None,
        description="List of statuses for the DNS records requested by the requirer."
    )


class RequirerDomains(BaseModel):
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
    uuid: str = Field(
        min_length=1,
        name="UUID",
        description="UUID for this domain.",
        examples="550e8400-e29b-41d4-a716-446655440000"
    )


class RequirerEntries(BaseModel):
    domain: str = Field(
        min_length=1,
        name="Domain",
        description="Domain name requested.",
        examples=["cloud.canonical.com", "staging.ubuntu.com"]
    )
    host_label: str = Field(
        min_length=1,
        name="Host label",
        description="Host label.",
        examples=["admin", "www"]
    )
    ttl: int = Field(
        default=None,
        name="TTL",
        description="The DNS time to live (seconds).",
        examples=[600, 1200]
    )
    record_class: RecordClass = Field(
        default=None,
        name="Record class",
        description="The DNS record class.",
        examples=[RecordClass.IN]
    )
    record_type: RecordType =Field(
        default=None,
        name="Record type",
        description="The DNS record type.",
        examples=[RecordType.A, RecordType.CNAME]
    )
    record_data: IPvAnyAddress = Field(
        name="Record data",
        description="The DNS record value.",
        examples=["91.189.91.47", "91.189.91.48"]
    )
    uuid: str = Field(
        min_length=1,
        name="UUID",
        description="UUID for this entry.",
        examples="550e8400-e29b-41d4-a716-446655440000"
    )


class DNSRecordRequirer(BaseModel):
    """List of domains for the provider to manage."""
    dns_domains: List[RequirerDomains] = Field(
        default=None,
        description="List of domains for the provider to manage."
    )
    dns_entries: List[RequirerEntries] = Field(
        default=None,
        description="List of DNS records for the provider to manage."
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for dns_record."""
    app: DNSRecordProvider


class RequirerSchema(DataBagSchema):
    """Requirer schema for dns_record."""
    app: DNSRecordRequirer
