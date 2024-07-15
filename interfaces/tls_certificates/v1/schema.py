"""
This file defines the schemas for the provider and requirer sides of the `tls_certificates` interface.

It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {
            "certificates": [
                {
                    "ca": "-----BEGIN CERTIFICATE----- ...",
                    "chain": [
                        "-----BEGIN CERTIFICATE----- ...",
                        "-----BEGIN CERTIFICATE----- ..."
                    ],
                    "certificate_signing_request": "-----BEGIN CERTIFICATE REQUEST----- ...",
                    "certificate": "-----BEGIN CERTIFICATE----- ..."
                }
            ]
        }
    RequirerSchema:
        unit: {
            "certificate_signing_requests": [
                {
                    "certificate_signing_request": "-----BEGIN CERTIFICATE REQUEST----- ...",
                    "ca": true
                }
            ]
        }
        app:  <empty>    
"""

from typing import List
from pydantic import BaseModel, Field, Json
from interface_tester.schema_base import DataBagSchema

class Certificate(BaseModel):    
    ca: str = Field(description="PEM encoded CA certificate.")
    chain: List[str] = Field(description="PEM encoded certificate chain.")
    certificate_signing_request: str = Field(description="PEM encoded certificate signing request.")
    certificate: str = Field(description="PEM encoded certificate.")

class CertificateRequest(BaseModel):
    certificate_signing_request: str = Field(description="PEM encoded certificate signing request.")
    ca: bool = Field(description="Whether the certificate is a CA certificate.")

class ProviderApplicationDataModel(BaseModel):
    certificates: Json[List[Certificate]] = Field(
        description="List of TLS Certificates."
    )

class RequirerUnitDataModel(BaseModel):
    certificate_signing_requests: Json[List[CertificateRequest]] = Field(
        description="List of Certificate Signing Requests."
    )

class RequirerApplicationDataModel(BaseModel):
    pass

class ProviderSchema(DataBagSchema):
    """Provider schema for TLS Certificates."""

    app: ProviderApplicationDataModel


class RequirerSchema(DataBagSchema):
    """Requirer schema for TLS Certificates."""

    unit: RequirerUnitDataModel
    app: RequirerApplicationDataModel
