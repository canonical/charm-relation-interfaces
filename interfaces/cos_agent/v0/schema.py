# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

"""This file defines the schemas for the provider and requirer sides of the cos_agent interface.
It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
Examples:
    ProviderSchema:
        app: <empty>
        # The value of `config` key is a json-dumped data.
        unit: {
                "config": {
                    "metrics_alert_rules": {
                      "groups": [
                        {
                          "name": "test_58b48ff0_zookeeper_cos_23790144_zinc",
                          "rules": [
                            {
                              "alert": "ZincTargetMissing",
                              "annotations": {
                                "description": "A Prometheus target has disappeared. An exporter might be crashed.\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}",
                                "summary": "Prometheus target missing (instance {{ $labels.instance}})"
                              },
                              "expr": "up{juju_application=\"zinc2\"} == 0",
                              "for": "0m",
                              "labels": {
                                "app_group": "cloud",
                                "juju_application": "zookeeper",
                                "juju_charm": "zookeeper",
                                "juju_model": "test",
                                "juju_model_uuid": "58b48ff0-608b-435f-83b9-ea643e0b98db",
                                "severity": "critical"
                              }
                            }
                          ]
                        }
                      ]
                    },
                    "log_alert_rules": {},
                    /* Dashboards list with base64 encoded, lzma-compressed, json-dumped dashboard data */
                    "dashboards": [
                      "/Td6WFoAAATm1rRGAgAhARYAAAB0L+Wj6hvVPXVdA…",
                      "/Td6WFoAAATm1rRGAgAhARYAAAB0L+Wj6hvVPXVdB…"
                    ],
                    "log_slots": [
                      "charmed-zookeeper:logs"
                    ],
                    "metrics_scrape_jobs": [{"job_name": "kafka_0", "path": "/metrics", "port": 9101}],
                  }
                }
    RequirerSchema:
        unit: <empty>
        app: <empty>
"""

import base64
import json
import lzma
from pydantic import BaseModel, Field, Json
from typing import Dict, List, Union
from interface_tester.schema_base import DataBagSchema


class GrafanaDashboard(str):
    """Grafana Dashboard encoded json; lzma-compressed."""

    # TODO Replace this with a custom type when pydantic v2 released (end of 2023 Q1?)
    # https://github.com/pydantic/pydantic/issues/4887
    @staticmethod
    def _serialize(raw_json: Union[str, bytes]) -> "GrafanaDashboard":
        if not isinstance(raw_json, bytes):
            raw_json = raw_json.encode("utf-8")
        encoded = base64.b64encode(lzma.compress(raw_json)).decode("utf-8")
        return GrafanaDashboard(encoded)

    def _deserialize(self) -> Dict:
        raw = lzma.decompress(base64.b64decode(self.encode("utf-8"))).decode()
        return json.loads(raw)

    def __repr__(self):
        """Return string representation of self."""
        return "<GrafanaDashboard>"


class NestedDataModel(BaseModel):
    """Nested model for `config` in ProviderUnitData."""

    class Config:
        arbitrary_types_allowed = True

    metrics_alert_rules: dict = Field(
        description="Generated by prometheus_scrape AlertRules from a list of Directory where the metrics rules are stored"
    )
    log_alert_rules: dict = Field(
        description="Generated by loki_push_api AlertRules from a list of Directory where the logs rules are stored"
    )
    dashboards: List[GrafanaDashboard] = Field(
        description="List of GrafanaDashboard objects. Each dashboard is base64 encoded, lzma-compressed, json-dumped dashboard data."
    )
    metrics_scrape_jobs: List[Dict] = Field(
        description="A list of dictionaries representing a prometheus_scrape-like data structure for jobs."
    )
    log_slots: List[str] = Field(
        description='List of snap slots to connect to for scraping logs. Each slot is in the form "snap-name:slot".'
    )


class ProviderUnitData(BaseModel):
    """Unit databag model for `cos-agent` relation."""

    config: Json[NestedDataModel] = Field(
        description='When dumped into a databag in JSON format, this configuration data will be nested under the key defaulted to "config".'
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for CosAgent."""

    unit: ProviderUnitData


class RequirerSchema(DataBagSchema):
    """Requirer schema for CosAgent."""
