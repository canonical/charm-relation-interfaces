# Copyright 2024 Canonical
# See LICENSE file for licensing details.

import json
from interface_tester import Tester
from scenario import State, Relation
from scenario.context import CharmEvents


def test_no_data_on_created():
    t = Tester()
    state_out = t.run("cos-agent-relation-created")
    t.assert_relation_data_empty()


def test_no_data_on_joined():
    t = Tester()
    state_out = t.run("cos-agent-relation-joined")
    t.assert_schema_valid()

def test_no_data_on_changed():
    t = Tester()
    state_out = t.run("cos-agent-relation-changed")
    t.assert_schema_valid()

valid_unit_data = {
    "config": {
        "metrics_alert_rules": {
            "groups": [
                {
                    "name": "welcome-lxd_f8768e19_kafka_jmx_missing_alerts",
                    "rules": [
                        {
                            "alert": "KafkaMissing",
                            "expr": "up == 0",
                            "for": "0m",
                            "labels": {
                                "severity": "critical",
                                "juju_model": "welcome-lxd",
                                "juju_model_uuid": "f8768e19-066a-449a-825b-20f060b99025",
                                "juju_application": "kafka",
                                "juju_charm": "kafka",
                            },
                            "annotations": {
                                "summary": "Prometheus target missing (instance {{ $labels.instance }})",
                                "description": "Kafka target has disappeared. An exporter might be crashed.\n  VALUE = {{ $value }}\n  LABELS = {{ $labels}}",
                            },
                        }
                    ],
                },
                {
                    "name": "welcome-lxd_f8768e19_kafka_jvm_filling_alerts",
                    "rules": [
                        {
                            "alert": "JvmMemoryFillingUp",
                            "expr": '(sum by (instance)(jvm_memory_bytes_used{area="heap"}) / sum by (instance)(jvm_memory_bytes_max{area="heap"})) * 100 > 80',
                            "for": "2m",
                            "labels": {
                                "severity": "warning",
                                "juju_model": "welcome-lxd",
                                "juju_model_uuid": "f8768e19-066a-449a-825b-20f060b99025",
                                "juju_application": "kafka",
                                "juju_charm": "kafka",
                            },
                            "annotations": {
                                "summary": "JVM memory filling up (instance {{ $labels.instance}})",
                                "description": "JVM memory is filling up (> 80%)\n  VALUE = {{ $value }}\n  LABELS ={{ $labels }}",
                            },
                        }
                    ],
                },
            ]
        },
        "log_alert_rules": {},
        "dashboards": [
            "/Td6WFoAAATm1rRGAgAhARYAAAB0L+Wj4af1GDxdAD2CgBccJ1Wse0YL0FXaPTB5Bgw6u7FoNcUn99tIdLOGVyat",
        ],
        "metrics_scrape_jobs": [
            {"job_name": "kafka_0", "path": "/metrics", "port": 9101}
        ],
        "log_slots": ["charmed-kafka:logs"],
    }
}

valid_unit_data["config"] = json.dumps(valid_unit_data["config"])

def test_on_changed_with_existing_valid_data():
    relation = Relation(
        endpoint="cos-agent",
        interface="cos-agent",
        local_unit_data=valid_unit_data,
    )
    t = Tester(State(relations=[relation]))
    state_out = t.run(CharmEvents.relation_changed(relation))
    t.assert_schema_valid()
