# Copyright 2024 Canonical
# See LICENSE file for licensing details.
"""This file defines the schemas for the provider sides of the cloudflared_route interface.
It exposes the interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {
          "tunnel_token_secret_id": "secret:csn5caau557j9bojn7rg",
          "nameserver": "1.1.1.1"
        }
"""

from pydantic import IPvAnyAddress, BaseModel
from interface_tester.schema_base import DataBagSchema


class CloudflaredRouteProvider(BaseModel):
    """List statuses for the DNS records informed by the requirer."""
    tunnel_token_secret_id: str
    nameserver: IPvAnyAddress | None = None


class ProviderSchema(DataBagSchema):
    """Provider schema for dns_record."""
    app: CloudflaredRouteProvider
