"""This file defines the schemas for the provider and requirer sides of the `certificate_transfer` interface.
It exposes two interface_tester.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
Examples:
    ProviderSchema:
        unit: {
            "certificates": [
                {
                    "certificate": "-----BEGIN CERTIFICATE----- ..."
                    "ca": "-----BEGIN CERTIFICATE----- ..."
                    "chain": [
                        "-----BEGIN CERTIFICATE----- ...",
                        "-----BEGIN CERTIFICATE----- ..."
                    ]
                },
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

class Certificate(BaseModel):
    certificate: str = Field(
        description="The certificate that was signed for a given CSR"
    )
    ca: str = Field(
        description="The certificate of the issuer that signed the given CSR"
    )
    chain: str = Field(
        description="The chain of certificates that originates from the CSR's certificate to the Root CA certificate"
    )

class CertificateTransferProviderAppData(BaseModel):
    certificates: List[Certificate]= Field(
        description="The list of certificates that will be transferred to a requirer"
    )

class ProviderSchema(DataBagSchema):
    """Provider schema for certificate_transfer."""
    unit: CertificateTransferProviderAppData


class RequirerSchema(DataBagSchema):
    """Requirer schema for certificate_transfer."""

