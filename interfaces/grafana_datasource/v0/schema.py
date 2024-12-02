from typing import Dict, Any

from pydantic import Json, BaseModel, Field

from interface_tester.schema_base import DataBagSchema


class GrafanaSourceData(BaseModel):
    model: str = Field(description="Name of the Juju model where the source is deployed.",
                       examples=['cos'])
    model_uuid: str = Field(description="UUID of the Juju model where the source is deployed.",
                            examples=["0000-0000-0000-0000"])
    application: str = Field(description="Name of the Juju model where the source is deployed.",
                             examples=['tempo', 'loki', 'prometheus'])
    type: str = Field(description="Type of the datasource.",
                      examples=['tempo', 'loki', 'prometheus'])
    extra_fields: Json[Any] = Field(
        description="Any datasource-type-specific additional configuration.")
    secure_extra_fields: Json[Any] = Field(
        description="Any secure datasource-type-specific additional configuration.")


class GrafanaSourceProviderAppData(BaseModel):
    """Application databag model for the requirer side of this interface."""
    grafana_source_data: Json[GrafanaSourceData]


class GrafanaSourceProviderUnitData(BaseModel):
    """Application databag model for the requirer side of this interface."""
    grafana_source_host: Json[GrafanaSourceData]


class ProviderSchema(DataBagSchema):
    """The schemas for the requirer side of this interface."""
    app: GrafanaSourceProviderAppData
    unit: GrafanaSourceProviderUnitData


class GrafanaSourceRequirerAppData(BaseModel):
    """Application databag model for the requirer side of this interface."""
    datasource_uids: Json[Dict[str, str]]


class RequirerSchema(DataBagSchema):
    """The schema for the provider side of this interface."""
    app: GrafanaSourceRequirerAppData
