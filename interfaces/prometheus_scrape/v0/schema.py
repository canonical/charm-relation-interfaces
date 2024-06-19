"""
This file defines the schemas for the provider and requirer sides of the `prometheus_scrape` interface.

It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        app: {
            "alert_rules": {
                "groups": [
                    {
                        "name": "an_alert_rule_group",
                        "rules": [
                            {
                                "alert": "SomethingIsUp",
                                "expr": "something_bad == 1",
                                "for": "0m",
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
        unit: {
            "prometheus_scrape_unit_address": "zinc-k8s-0.zinc-k8s-endpoints.cos.svc.cluster.local",
            "prometheus_scrape_unit_name": "zinc-k8s/0"
            "prometheus_scrape_unit_path": null

        }
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field, Json
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
    groups: List[AlertGroupModel] = Field(description="List of alert rule groups.")


class ScrapeStaticConfigModel(BaseModel):
    class Config:
        extra = "allow"

    targets: List[str] = Field(
        description='List of scrape targets. Accepts wildcard ("*")'
    )
    labels: Optional[Dict[str, str]] = Field(
        description="Optional labels for the scrape targets", default=None
    )


class ScrapeJobModel(BaseModel):
    class Config:
        extra = "allow"

    job_name: Optional[str] = Field(
        description="Name of the Prometheus scrape job, each job must be given a unique name &  should be a fixed string (e.g. hardcoded literal)",
        default=None,
    )
    metrics_path: Optional[str] = Field(
        description="Path for metrics scraping.", default=None
    )
    static_configs: List[ScrapeStaticConfigModel] = Field(
        description="List of static configurations for scrape targets."
    )


class ScrapeMetadataModel(BaseModel):
    class Config:
        extra = "allow"

    model: str = Field(description="Juju model name.")
    # in pydantic v2, `model_` is a protected namespace
    juju_model_uuid: str = Field(description="Juju model UUID.", alias="model_uuid")
    application: str = Field(description="Juju application name.")
    unit: str = Field(description="Juju unit name.")


class ApplicationDataModel(BaseModel):
    alert_rules: Json[AlertRulesModel] = Field(
        description="Alert rules provided by the charm. By default, loaded from "
        "`<charm_parent_dir>/prometheus_alert_rules`."
    )
    scrape_jobs: Json[List[ScrapeJobModel]] = Field(
        description="List of Prometheus scrape job configurations specifying metrics scraping targets."
    )
    scrape_metadata: Json[ScrapeMetadataModel] = Field(
        description="Metadata providing information about the Juju topology."
    )


class UnitDataModel(BaseModel):
    class Config:
        extra = "allow"

    prometheus_scrape_unit_address: str = Field(
        description="The address provided by the unit for Prometheus scraping. "
        "This address is where Prometheus can retrieve metrics data from the unit."
    )
    prometheus_scrape_unit_name: str = Field(
        description="The name provided by the unit for Prometheus scraping. "
        "This name uniquely identifies the unit as a target for Prometheus to collect metrics data."
    )
    prometheus_scrape_unit_path: Optional[str] = Field(
        description="An optional path provided by the unit for Prometheus scraping. "
        "It is present when the provider charm is backed by an Ingress or a Proxy."
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for Prometheus Scrape."""

    app: ApplicationDataModel
    unit: UnitDataModel


class RequirerSchema(DataBagSchema):
    """Requirer schema for Prometheus Scrape."""
