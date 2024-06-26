"""This file defines the schemas for the provider and requirer sides of the `certificate_transfer` interface.
It exposes two interface_tester.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
Examples:
    ProviderSchema:
        unit: {
            "certificates": [
                "-----BEGIN CERTIFICATE----- ...",
                "-----BEGIN CERTIFICATE----- ..."
            ]
        }
        app: <empty>
    RequirerSchema:
        unit: <empty>
        app:  <empty>
"""
from pydantic import BaseModel, Field
from typing import List
from interface_tester.schema_base import DataBagSchema

class CertificateTransferProviderAppData(BaseModel):
    certificates: List[str]= Field(
        description="The list of certificates that will be transferred to a requirer"
    )

class ProviderSchema(DataBagSchema):
    """Provider schema for certificate_transfer."""
    unit: CertificateTransferProviderAppData


class RequirerSchema(DataBagSchema):
    """Requirer schema for certificate_transfer."""

