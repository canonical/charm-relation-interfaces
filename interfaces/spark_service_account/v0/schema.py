"""This file defines the schemas for the provider and requirer sides of this relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from pydantic import BaseModel, Field
from interface_tester.schema_base import DataBagSchema


class SparkServiceAccountProviderAppData(BaseModel):
    service_account: str = Field(
        alias="service-account",
        description="The name of the service account to be created and the namespace in which the service account is to be created.",
        examples=["test_namespace:test_service_account"],
        title="Service Account",
    )

    secret_spark_properties: str = Field(
        alias="secret-spark-properties",
        description="The name of the Spark Properties secret to use. The secret contains [spark-properties], which is the list of different Spark properties that are associated with this service account. ",
        examples=["secret://59060ecc-0495-4a80-8006-5f1fc13fd783/cjqub7fubg2s77p3niog"],
        title="Spark Properties Secret Name",
    )


class SparkServiceAccountRequirerAppData(BaseModel):
    service_account: str = Field(
        alias="service-account",
        description="The name of the service account to be created and the namespace in which the service account is to be created.",
        examples=["test_namespace:test_service_account"],
        title="Service Account",
    )

    requested_secrets: list[str] = Field(
        alias="requested-secrets",
        description="Any provider field which should be transfered as Juju Secret. This field is auto-populated by the data-interfaces lib.",
        examples=[["spark-properties"]],
        title="Requested secrets",
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: SparkServiceAccountProviderAppData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    app: SparkServiceAccountRequirerAppData
