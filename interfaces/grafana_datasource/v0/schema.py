from typing import Dict, Any, Optional

from interface_tester.schema_base import DataBagSchema
from pydantic import Json, BaseModel, Field


class GrafanaSourceData(BaseModel):
    model: str = Field(description="Name of the Juju model where the source is deployed.",
                       examples=['cos'])
    model_uuid: str = Field(description="UUID of the Juju model where the source is deployed.",
                            examples=["0000-0000-0000-0000"])
    application: str = Field(description="Name of the Juju model where the source is deployed.",
                             examples=['tempo', 'loki', 'prometheus'])
    type: str = Field(description="Type of the datasource.",
                      examples=['tempo', 'loki', 'prometheus'])
    extra_fields: Optional[Json[Any]] = Field(
        description="Any datasource-type-specific additional configuration.")
    secure_extra_fields: Optional[Json[Any]] = Field(
        description="Any secure datasource-type-specific additional configuration.")


class GrafanaSourceProviderAppData(BaseModel):
    """Application databag model for the requirer side of this interface."""
    grafana_source_data: Json[GrafanaSourceData]


class GrafanaSourceProviderUnitData(BaseModel):
    """Application databag model for the requirer side of this interface."""
    grafana_source_host: str = Field(
        description="Hostname of a source server.",
        examples=['localhost:80']
    )


class ProviderSchema(DataBagSchema):
    """The schemas for the requirer side of this interface."""
    app: GrafanaSourceProviderAppData
    unit: GrafanaSourceProviderUnitData


class GrafanaSourceRequirerAppData(BaseModel):
    """Application databag model for the requirer side of this interface."""
    datasource_uids: Json[Dict[str, str]]
    grafana_uid: str = Field(
        description="UID of the requirer application.",
        examples=['foo-0000-0000-0000-0000-grafana-1']
    )


class RequirerSchema(DataBagSchema):
    """The schema for the provider side of this interface."""
    app: GrafanaSourceRequirerAppData
