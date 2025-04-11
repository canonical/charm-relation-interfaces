# Copyright 2025 Canonical
# See LICENSE file for licensing details.

from interface_tester.schema_base import DataBagSchema
from pydantic import Field


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    endpoints: str = Field(
        description="Comma separated list of etcd endpoints",
        title="etcd Endpoints",
        examples=["etcd1:2379,etcd2:2379"],
    )

    version: str = Field(
        description="etcd version",
        title="etcd Version",
        examples=["3.5.18"],
    )

    secret_tls: str = Field(
        description="Secret URI containing the tls-ca",
        title="TLS Secret URI",
        examples=["secret://12312323112313123213"],
    )

    secret_user: str = Field(
        description="Secret URI containing the etcd user information",
        title="User Secret URI",
        examples=["secret://12312323112313123213"],
    )


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    prefix: str = Field(
        description="The prefix of the range of keys requested",
        title="Key Prefix",
        examples=["/my/keys"],
    )

    secret_mtls: str = Field(
        description="Secret URI containing the client certificate",
        title="mTLS Secret URI",
        examples=["secret://12312323112313123213"],
    )

    requested_secrets: str = Field(
        description="The fields required to be a secret.",
        title="Requested Secrets",
        examples='["username", "uris", "tls", "tls-ca"]',
    )

    provided_secrets: str = Field(
        description="The fields provided as secrets",
        title="Provided Secrets",
        examples='["mtls-cert"]',
    )
