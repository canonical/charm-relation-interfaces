"""
This file defines the schemas for the provider and requirer sides of the `prometheus_scrape` interface.

It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        application_data: {
            "alert_rules": {
                "groups": [
                    {
                        "name": "an_alert_rule_group",
                        "rules": [
                            {
                                "alert": "SomethingIsUp",
                                "expr": "something_bad == 1",
                                "for_": "0m",
                                "labels": {
                                    "some-label": "some-value"
                                },
                                "annotations": {
                                    "some-annotation": "some-other-value"
                                }
                            }
                        ]
                    }
                ]
            },
            "scrape_jobs": [
                {
                    "metrics_path": "/metrics",
                    "static_configs": [
                        {
                            "targets": [
                                "*:4080"
                            ]
                        }
                    ]
                }
            ],
            "scrape_metadata": {
                "model": "cos",
                "model_uuid": "c2e9f4d5-dcb3-4870-8509-330eb9745ee8",
                "application": "zinc-k8s",
                "unit": "zinc-k8s/0",
                "charm_name": "zinc-k8s"
            }
        },
        related_units: {
            "zinc-k8s/0": {
                "data": {
                    "prometheus_scrape_unit_address": "zinc-k8s-0.zinc-k8s-endpoints.cos.svc.cluster.local",
                    "prometheus_scrape_unit_name": "zinc-k8s/0"
                }
            }
        }
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from interface_tester.schema_base import DataBagSchema


class AlertRuleModel(BaseModel):
    alert: str = Field(description="The name of the alert rule.")
    expr: str = Field(description="The expression for the alert rule.")
    for_: str = Field(
        alias="for",
        description="The duration for which the conditions must be true for the alert to be firing.",
    )
    labels: Dict[str, str] = Field(description="Labels associated with the alert rule.")
    annotations: Dict[str, str] = Field(
        description="Annotations associated with the alert rule."
    )


class AlertGroupModel(BaseModel):
    name: str = Field(description="The name of the alert group.")
    rules: List[AlertRuleModel] = Field(
        description="List of alert rules within the group."
    )


class AlertRulesModel(BaseModel):
    groups: List[AlertGroupModel]


class ScrapeStaticConfigModel(BaseModel):
    targets: List[str] = Field(
        description='List of scrape targets. Accepts wildcard ("*")'
    )
    labels: Optional[Dict[str, str]] = Field(
        description="Optional labels for the scrape targets", default=None
    )

    class Config:
        extra = "allow"


class ScrapeJobModel(BaseModel):
    job_name: Optional[str] = Field(
        description="Name of the Prometheus scrape job, each job must be given a unique name",
        default=None,
    )
    metrics_path: str = Field(description="Path for metrics scraping.")
    static_configs: List[ScrapeStaticConfigModel]

    class Config:
        extra = "allow"


class ScrapeMetadataModel(BaseModel):
    model: str
    model_uuid: str
    application: str
    unit: str


class ApplicationDataModel(BaseModel):
    alert_rules: AlertRulesModel
    scrape_jobs: List[ScrapeJobModel]
    scrape_metadata: ScrapeMetadataModel


class UnitDataModel(BaseModel):
    prometheus_scrape_unit_address: str
    prometheus_scrape_unit_name: str


class ProviderSchema(DataBagSchema):
    """Provider schema for Prometheus Scrape."""

    app: ApplicationDataModel
    unit: UnitDataModel


class RequirerSchema(DataBagSchema):
    """Requirer schema for Prometheus Scrape."""
