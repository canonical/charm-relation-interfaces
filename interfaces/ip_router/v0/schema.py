"""This file defines the schemas for the provider and requirer sides of the `ip_router` interface.
It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
Examples:
    ProviderSchema:
        unit: <empty>
        app: {
              "networks": [
                {
                  "network": "192.168.250.0/24",
                  "gateway": "192.168.250.1",
                  "routes": [
                    {
                      "destination": "172.250.0.0/16",
                      "gateway": "192.168.250.3"
                    }
                  ]
                },
                {
                  "network": "192.168.252.0/24",
                  "gateway": "192.168.252.1",

                },
                {
                  "network": "192.168.251.0/24",
                  "gateway": "192.168.251.1/24"
                }
              ]
            }
    RequirerSchema:
        unit: <empty>
        app:  {
              "networks": [
                {
                  "network": "192.168.250.0/24",
                  "gateway": "192.168.250.1",
                  "routes": [
                    {
                      "destination": "172.250.0.0/16",
                      "gateway": "192.168.250.3"
                    }
                  ]
                }
              ]
            }
"""

from pydantic import BaseModel, IPvAnyAddress, IPvAnyNetwork
from typing import Optional, List
from interface_tester.schema_base import DataBagSchema


class Route(BaseModel):
    destination: IPvAnyAddress
    gateway: IPvAnyAddress


class IPNetwork(BaseModel):
    network: IPvAnyNetwork
    gateway: IPvAnyAddress
    routes: Optional[List[Route]]


class IPRouterProviderAppData(BaseModel):
    networks: List[IPNetwork]


class IPRouterRequirerAppData(BaseModel):
    networks: List[IPNetwork]


class ProviderSchema(DataBagSchema):
    """Provider schema for ip_router."""
    app: IPRouterProviderAppData


class RequirerSchema(DataBagSchema):
    """Requirer schema for ip_router."""
    app: IPRouterRequirerAppData
