# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

"""This file defines the schemas for the provider and requirer sides of the cos_agent interface.
It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
Examples:
    ProviderSchema:
        app: <empty>
        unit: "config": {
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
                            ],
                        },
                        ],
                },
                "log_alert_rules": {},
                "dashboards": [
                    "/Td6WFoAAATm1rRGAgAhARYAAAB0L+Wj6hvVPXVdA…",
                    "/Td6WFoAAATm1rRGAgAhARYAAAB0L+Wj6hvVPXVdB…",
                ],
                "log_slots": ["charmed-zookeeper:logs"]
            }
    RequirerSchema:
        unit: <empty>
        app: <empty>
"""

import base64
import json
import lzma
from pydantic import BaseModel
from typing import ClassVar, Dict, List, Union, Optional
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


class CosAgentProviderUnitData(BaseModel):
    """Unit databag model for `cos-agent` relation."""

    # The following entries are the same for all units of the same principal.
    # Note that the same grafana agent subordinate may be related to several apps.
    # this needs to make its way to the gagent leader
    metrics_alert_rules: dict
    log_alert_rules: dict
    dashboards: List[GrafanaDashboard]

    # The following entries may vary across units of the same principal app.
    # this data does not need to be forwarded to the gagent leader
    metrics_scrape_jobs: List[Dict]
    log_slots: List[str]

    # when this whole datastructure is dumped into a databag, it will be nested under this key.
    # while not strictly necessary (we could have it 'flattened out' into the databag),
    # this simplifies working with the model.
    KEY: ClassVar[str] = "config"


class CosAgentPeersUnitData(BaseModel):
    """Unit databag model for `cluster` cos-agent machine charm peer relation."""

    # We need the principal unit name and relation metadata to be able to render identifiers
    # (e.g. topology) on the leader side, after all the data moves into peer data (the grafana
    # agent leader can only see its own principal, because it is a subordinate charm).
    principal_unit_name: str
    principal_relation_id: str
    principal_relation_name: str

    # The only data that is forwarded to the leader is data that needs to go into the app databags
    # of the outgoing o11y relations.
    metrics_alert_rules: Optional[dict]
    log_alert_rules: Optional[dict]
    dashboards: Optional[List[GrafanaDashboard]]

    # when this whole datastructure is dumped into a databag, it will be nested under this key.
    # while not strictly necessary (we could have it 'flattened out' into the databag),
    # this simplifies working with the model.
    KEY: ClassVar[str] = "config"

    @property
    def app_name(self) -> str:
        """Parse out the app name from the unit name.

        TODO: Switch to using `model_post_init` when pydantic v2 is released?
          https://github.com/pydantic/pydantic/issues/1729#issuecomment-1300576214
        """
        return self.principal_unit_name.split("/")[0]


class ProviderSchema(DataBagSchema):
    """Provider schema for CosAgent."""

    unit: CosAgentProviderUnitData


class RequirerSchema(DataBagSchema):
    """Requirer schema for CosAgent."""

    unit: CosAgentPeersUnitData
