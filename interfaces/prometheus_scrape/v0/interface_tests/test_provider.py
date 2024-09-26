# Copyright 2024 Canonical
# See LICENSE file for licensing details.

import json
from interface_tester import Tester
from scenario import Relation, State
from scenario.context import CharmEvents


def test_no_data_on_created():
    t = Tester()
    state_out = t.run("prometheus-scrape-relation-created")
    t.assert_relation_data_empty()


def test_no_data_on_joined():
    t = Tester()
    state_out = t.run("prometheus-scrape-relation-joined")
    t.assert_schema_valid()


def test_no_data_on_changed():
    t = Tester()
    state_out = t.run("prometheus-scrape-relation-changed")
    t.assert_relation_data_empty()


valid_app_data = {
    "alert_rules": {
        "groups": [
            {
                "name": "critical_alerts",
                "rules": [
                    {
                        "alert": "DiskSpaceExceeded",
                        "expr": "disk_usage > 90",
                        "for": "5m",
                        "labels": {"severity": "critical", "team": "ops"},
                        "annotations": {
                            "summary": "Disk space exceeded alert",
                            "description": "The disk usage on the server has exceeded 90% for the last 5 minutes.",
                        },
                    }
                ],
            }
        ]
    },
    "scrape_jobs": [
        {
            "metrics_path": "/metrics",
            "static_configs": [
                {
                    "targets": ["server1:8080", "server2:8080"],
                    "labels": {"job": "server_metrics"},
                }
            ],
        }
    ],
    "scrape_metadata": {
        "model": "example-model",
        "model_uuid": "12345678-abcd-1234-efgh-1234567890ab",
        "application": "example-app",
        "unit": "example-app/0",
        "charm_name": "example-charm",
    },
}
valid_unit_data = {
    "prometheus_scrape_unit_address": "example-app-0.example-model-endpoints.default.svc.cluster.local",
    "prometheus_scrape_unit_name": "example-app/0",
    "prometheus_scrape_unit_path": '',
}
valid_app_data["scrape_metadata"] = json.dumps(valid_app_data["scrape_metadata"])
valid_app_data["scrape_jobs"] = json.dumps(valid_app_data["scrape_jobs"])
valid_app_data["alert_rules"] = json.dumps(valid_app_data["alert_rules"])

def test_on_changed_with_existing_valid_data():
    relation = Relation(
        endpoint="prometheus_scrape",
        interface="prometheus_scrape",
        local_app_data=valid_app_data,
        local_unit_data=valid_unit_data,
    )
    t = Tester(State(relations=[relation]))
    state_out = t.run(CharmEvents.relation_changed(relation))
    t.assert_schema_valid()
