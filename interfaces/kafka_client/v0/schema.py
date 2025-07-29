"""This file defines the schemas for the provider and requirer sides of the kafka_client interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from enum import Enum
from typing import Optional

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field, field_validator


class ExtraUserRole(str, Enum):
    admin = "admin"
    consumer = "consumer"
    producer = "producer"


class KafkaProviderData(BaseModel):
    """The databag for the provider side of this interface."""

    topic: str = Field(
        description="The topic that has been made available to the relation user. Name defined in the Requirer's topic field",
        examples=["topic-1", "appname-*"],
        title="Topic name",
    )

    username: str = Field(
        description="Username for connecting to the Kafka cluster",
        examples=["relation-14"],
        title="Kafka SASL/SCRAM username",
    )

    password: str = Field(
        description="Password for connecting to the Kafka cluster",
        examples=["alphanum-32byte-random"],
        title="Kafka SASL/SCRAM password",
    )

    endpoints: str = Field(
        description="A list of endpoints used to connect to the topic",
        examples=["10.141.78.155:9092,10.141.78.62:9092,10.141.78.186:9092"],
        title="Kafka server endpoints",
    )

    consumer_group_prefix: Optional[str] = Field(
        None,
        alias="consumer-group-prefix",
        description="A prefix for wildcard consumer-group IDs that have been granted permissions",
        examples=["relation-14-"],
        title="Kafka consumer group prefix",
    )

    zookeeper_uris: Optional[str] = Field(
        None,
        alias="consumer-group-prefix",
        description="A comma-seperated list of Zookeeper server URIs, and Kafka cluster zNode",
        examples=["10.141.78.155:2181,10.141.78.62:2181,10.141.78.186:2181/kafka"],
        title="Zookeeper URIs",
    )

    entity_name: Optional[str] = Field(
        None,
        alias="entity-name",
        description="Name for the requested custom entity",
        examples=["custom-role"],
        title="Entity name",
    )

    entity_password: Optional[str] = Field(
        None,
        alias="entity-password",
        description="Password for the requested custom entity",
        examples=["alphanum-32byte-random"],
        title="Entity password",
    )


class KafkaRequirerData(BaseModel):
    """The databag for the requirer side of this interface."""

    topic: str = Field(
        description="The topic name access requested by the requirer",
        examples=["topic-1", "appname-*"],
        title="Topic name",
    )

    consumer_group_prefix: Optional[str] = Field(
        None,
        alias="consumer-group-prefix",
        description="A prefix for wildcard consumer-group IDs that have been granted permissions",
        examples=["relation-14-"],
        title="Kafka consumer group prefix",
    )

    extra_user_roles: Optional[str] = Field(
        None,
        alias="extra-user-roles",
        description="Any extra user roles requested by the requirer",
        examples=[
            "consumer",
            "producer",
            "admin",
            "consumer,producer",
            "consumer,admin",
            "producer,admin",
            "consumer,producer,admin"
        ],
        title="Extra user roles",
    )

    extra_group_roles: Optional[str] = Field(
        None,
        alias="extra-group-roles",
        description="Any extra group roles requested by the requirer",
        examples=["charmed_read"],
        title="Extra group roles",
    )

    entity_type: Optional[str] = Field(
        None,
        alias="entity-type",
        description="Type of the requested entity (user / group)",
        examples=["USER", "GROUP"],
        title="Entity type",
    )

    entity_permissions: Optional[str] = Field(
        None,
        alias="entity-permissions",
        description="List of permissions to assign to the custom entity, in JSON format",
        examples=["[{\"resource_name\": \"messages\", \"resource_type\": \"TOPIC\", \"privileges\": [\"READ\"]}]"],
        title="Entity permissions",
    )

    @field_validator("extra_user_roles", mode="before")
    @classmethod
    def capitalize(cls, value: str) -> str:
        extra_roles = value.split(",")

        for role in extra_roles:
            if role not in ExtraUserRole:
                raise ValueError(f"Role {role} is not valid.")

        return value


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""

    app: KafkaProviderData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""

    app: KafkaRequirerData
