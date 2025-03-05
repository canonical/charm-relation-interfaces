# Copyright 2025 Canonical
# See LICENSE file for licensing details.

from interface_tester.schema_base import DataBagSchema
from pydantic import Field


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    # comma separated list of etcd endpoints
    endpoints: str = Field(
        description="Comma separated list of etcd endpoints",
        title="etcd Endpoints",
        examples=["http://etcd1:2379,http://etcd2:2379"],
    )
    # etcd version
    version: str = Field(
        description="etcd version",
        title="etcd Version",
        examples=["3.5.18"],
    )
    # sercet uri containing the tls-ca
    secret_tls: str = Field(
        description="Secret URI containing the tls-ca",
        title="TLS Secret URI",
        examples=["secret://12312323112313123213"],
    )


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    # The common name of the client certificate
    common_name: str = Field(
        description="The common name of the client certificate",
        title="Common Name",
        examples=["etcd-client"],
    )
    # The prefix of the range of keys requested
    prefix: str = Field(
        description="The prefix of the range of keys requested",
        title="Key Prefix",
        examples=["/my/keys"],
    )
    # The CA chain signing the client certificate
    secret_mtls: str = Field(
        description="Secret URI containing the client CA chain",
        title="mTLS Secret URI",
        examples=["secret://12312323112313123213"],
    )
    # The fields required to be a secret. Needs to contain "tls-ca"
    requested_secrets: list[str] = Field(
        description="The fields required to be a secret. Needs to contain 'tls-ca'",
        title="Requested Secrets",
        examples=[["tls-ca"]],
    )
