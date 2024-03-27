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
          ],
          dns-entries: ‘[
            {
              "domain": "canonical.com",
              "host_label": "admin",
              "ttl": 600,
              "record_class": "IN",
              "record_type": "A",
              "record_data": "91.189.91.48"
            },{
              "domain": "canonical.com",
              "host_label": "www",
              "record_data": "91.189.91.47"
            }
        ]’

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
          ],
          dns-entries: [
            {
              "domain": "cloud.canonical.com",
              "host_label": "admin",
              "record_type": "A",
              "status": "denied",
              "status_description": "incorrect username & password"
            },
            {
              "domain": "canonical.com",
              "host_label": "www",
              "status": "approved"
            }
        ]

        }
"""

from enum import Enum
from typing import List, Optional
from pydantic import IPvAnyAddress, BaseModel, Field

from interface_tester.schema_base import DataBagSchema


class Status(str, Enum):
    """Represent the status values."""

    APPROVED = "approved"
    DENIED = "denied"


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
    CH = "CH"
    HS = "HS"


class ProviderDomains(BaseModel):
    uuid: str = Field(
        min_length=1,
        name="UUID",
        description="UUID for this domain as specified by the requirer.",
        examples="550e8400-e29b-41d4-a716-446655440000"
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


class ProviderEntries(BaseModel):
    uuid: str = Field(
        min_length=1,
        name="UUID",
        description="UUID for this entry as specified by the requirer.",
        examples="550e8400-e29b-41d4-a716-446655440000"
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
    dns_domains: Optional[List[ProviderDomains]] = Field(
        description="List statuses for the domains requested by the requirer."
    )
    dns_entries: Optional[List[ProviderEntries]] = Field(
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
        status_description="Host label.",
        examples=["admin", "www"]
    )
    ttl: Optional[int] = Field(
        name="TTL",
        status_description="The DNS time to live.",
        examples=[600, 1200]
    )
    record_class: Optional[RecordClass] = Field(
        name="Record class",
        status_description="The DNS record class.",
        examples=[RecordClass.IN, RecordClass.HS]
    )
    record_type: Optional[RecordType] =Field(
        name="Record type",
        status_description="The DNS record type.",
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


class DnsRecordRequirer(BaseModel):
    """List of domains for the provider to manage."""
    dns_domains: Optional[List[RequirerDomains]] = Field(
        description="List of domains for the provider to manage."
    )
    dns_entries: Optional[List[RequirerEntries]] = Field(
        description="List of DNS records for the provider to manage."
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for dns_record."""
    app: DnsRecordProvider


class RequirerSchema(DataBagSchema):
    """Requirer schema for dns_record."""
    app: DnsRecordRequirer
