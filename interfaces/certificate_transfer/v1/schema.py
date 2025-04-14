"""This file defines the schemas for the provider and requirer sides of the `certificate_transfer` interface.
It exposes two interface_tester.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
Examples:
    ProviderSchema:
        unit: <empty>
        app: {
            "certificates": [
                "-----BEGIN CERTIFICATE----- ...",
                "-----BEGIN CERTIFICATE----- ..."
            ]
        }
    RequirerSchema:
        unit: <empty>
        app:  <empty>
"""

from pydantic import BaseModel, Field
from typing import Set
from interface_tester.schema_base import DataBagSchema


class CertificateTransferProviderAppData(BaseModel):
    certificates: Set[str] = Field(
        description="The set of certificates that will be transferred to a requirer"
    )
    version: int = Field(
        description="The version of the interface used in this databag",
        default=1
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for certificate_transfer."""

    app: CertificateTransferProviderAppData


class CertificateTransferRequirerAppData(BaseModel):
    version: int = Field(
        description="The version of the interface used by this requirer",
        default=1
    )


class RequirerSchema(DataBagSchema):
    """Requirer schema for certificate_transfer."""

    app: CertificateTransferRequirerAppData
