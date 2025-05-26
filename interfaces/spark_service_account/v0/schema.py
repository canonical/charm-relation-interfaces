"""This file defines the schemas for the provider and requirer sides of this relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from typing import List
from pydantic import BaseModel, Field
from interface_tester.schema_base import DataBagSchema


class SparkServiceAccountProviderAppData(BaseModel):
    service_account: str = Field(
        alias="service-account",
        description="The name of the service account to be created and the namespace in"
        " which the service account is to be created.",
        examples=["test_namespace:test_service_account"],
        title="Service Account",
    )

    secret_extra: str = Field(
        alias="secret-extra",
        description="The name of the Spark properties and K8s resource manifest secret "
        "to use. The secret contains 1. `spark-properties`, the list of different Spark"
        " properties that are associated with this service account and 2. "
        "`resource-manifest`, which contains the YAML dump of the K8s service account.",
        examples=["secret://59060ecc-0495-4a80-8006-5f1fc13fd783/cjqub7fubg2s77p3niog"],
        title="Spark properties and K8s resource manifest secret",
    )


class SparkServiceAccountRequirerAppData(BaseModel):
    service_account: str = Field(
        alias="service-account",
        description="The name of the service account to be created and the namespace in"
        " which the service account is to be created.",
        examples=["test_namespace:test_service_account"],
        title="Service Account",
    )

    requested_secrets: List[str] = Field(
        alias="requested-secrets",
        description="Any provider field which should be transfered as Juju Secret. This"
        " field is auto-populated by the data-interfaces lib.",
        examples=[["spark-properties", "resource-manifest"]],
        title="Requested secrets",
    )

    skip_creation: bool = Field(
        alias="skip-creation",
        description="Define whether the providing charm should skip the creation of the"
        " service account requested.",
        title="Skip creation",
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: SparkServiceAccountProviderAppData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    app: SparkServiceAccountRequirerAppData
