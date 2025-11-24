"""This file defines the schemas for the provider and requirer sides of the s3 v1 relation
interface.
"""

from enum import IntEnum, Enum
from typing import List, Optional

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field


class S3URIStyleEnum(str, Enum):
    path = "path"
    host = "host"


class S3APIVersion(IntEnum):
    v2 = 2
    v4 = 4


class S3ProviderAppData(BaseModel):
    """Data expected on the provider side for the s3 v1 interface."""


    bucket: Optional[str] = Field(
        description="The bucket/container name delivered by the provider.",
        examples=["minio"],
        title="Bucket name",
    )

    lib_version: str = Field(
        alias="lib-version",
        description="The S3 lib version used by the provider charm.",
        examples=["1.10"],
        title="S3 lib version",
    )

    secret_extra: str = Field(
        alias="secret-extra",
        description=(
            "A Juju Secret ID that points to a secret containing access-key and"
            " secret-key for connecting to the object storage."
        ),
        examples=["secret://91f805c5-5b49-47a3-8e7b-70befa766caf/d40rbhnmp25c76d6bdn0"],
        title="Credentials Secret ID",
    )

    path: Optional[str] = Field(
        description="The path inside the bucket/container to store objects.",
        examples=["my/path/"],
        title="Path",
    )

    endpoint: Optional[str] = Field(
        description="The endpoint used to connect to the object storage.",
        examples=["https://minio-endpoint/"],
        title="Endpoint URL",
    )

    region: Optional[str] = Field(
        description="The region used to connect to the object storage.",
        examples=["us-east-1"],
        title="Region",
    )

    s3_uri_style: Optional[S3URIStyleEnum] = Field(
        alias="s3-uri-style",
        description="The S3 protocol specific bucket path lookup type.",
        examples=["path", "host"],
        title="S3 URI Style",
    )

    storage_class: Optional[str] = Field(
        alias="storage-class",
        description="Storage Class for objects uploaded to the object storage.",
        examples=["glacier"],
        title="Storage Class",
    )

    tls_ca_chain: Optional[List[str]] = Field(
        alias="tls-ca-chain",
        description="The complete CA chain, which can be used for HTTPS validation.",
        examples=[["base64-encoded-ca-chain=="]],
        title="TLS CA Chain",
    )

    s3_api_version: Optional[S3APIVersion] = Field(
        alias="s3-api-version",
        description="S3 protocol specific API signature.",
        examples=[2, 4],
        title="S3 API signature",
    )

    attributes: Optional[List[str]] = Field(
        description="The custom metadata (HTTP headers).",
        examples=[
            [
                "Cache-Control=max-age=90000,min-fresh=9000",
                "X-Amz-Server-Side-Encryption-Customer-Key=CuStoMerKey=",
            ]
        ],
        title="Custom metadata",
    )


class S3RequirerAppData(BaseModel):
    """Data expected on the requirer side for the s3 v1 interface."""

    bucket: Optional[str] = Field(
        description="The name of the bucket/container requested by the requirer.",
        examples=["minio"],
        title="Bucket",
    )

    lib_version: str = Field(
        alias="lib-version",
        description="The desired S3 lib version the requirer expects.",
        examples=["1.10"],
        title="S3 lib version",
    )

    path: Optional[str] = Field(
        description="The path inside the bucket/container to store objects.",
        examples=["my/path/"],
        title="Path",
    )

    requested_secrets: str = Field(
        alias="requested-secrets",
        description="Any provider field which should be transferred as a Juju Secret.",
        examples=[["access-key", "secret-key"]],
        title="Requested secrets",
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: S3ProviderAppData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    app: S3RequirerAppData
