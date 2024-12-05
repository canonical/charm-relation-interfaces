from typing import List

from interface_tester.schema_base import DataBagSchema
from pydantic import Json, BaseModel, Field


class GrafanaDatasource(BaseModel):
    type: str = Field(description="Type of the datasource, typically one of "
                                  "https://grafana.com/docs/grafana/latest/datasources/#built-in-core-data-sources.",
                      examples=["tempo", "loki", "prometheus", "elasticsearch"])
    uid: str = Field(description="Grafana datasource UID, as assigned by Grafana.")
    grafana_uid: str = Field(description="Grafana UID.")


class GrafanaSourceAppData(BaseModel):
    """Application databag model for the requirer side of this interface."""
    datasources: Json[List[GrafanaDatasource]]


class ProviderSchema(DataBagSchema):
    """The schemas for the requirer side of this interface."""
    app: GrafanaSourceAppData


class RequirerSchema(DataBagSchema):
    """The schemas for the provider side of this interface."""
    app: GrafanaSourceAppData
