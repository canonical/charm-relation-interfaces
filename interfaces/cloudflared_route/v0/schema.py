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

import typing

from pydantic import IPvAnyAddress, BaseModel
from interface_tester.schema_base import DataBagSchema


class CloudflaredRouteProvider(BaseModel):
    """Provider application databag schema for cloudflared_route integration."""
    tunnel_token_secret_id: str
    nameserver: typing.Optional[IPvAnyAddress] = None


class ProviderSchema(DataBagSchema):
    """Provider schema for cloudflared_route integration."""
    app: CloudflaredRouteProvider
