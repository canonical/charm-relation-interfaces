# Copyright 2024 Canonical
# See LICENSE file for licensing details.
import json

from interface_tester.interface_test import Tester
from scenario import Relation, State


def test_validation_fails_with_missing_role():
    tester = Tester(
        state_in=State(
            relations=[
                Relation(
                    endpoint="pyroscope_cluster",
                    interface="pyroscope_cluster",
                    remote_app_name="worker",
                    remote_app_data={},
                    remote_units_data={
                        0: {
                            "juju_topology": json.dumps(
                                {
                                    "application": "worker",
                                    "unit": "worker/0",
                                    "charm_name": "worker",
                                }
                            ),
                            "address": json.dumps("192.0.2.1"),
                        }
                    },
                )
            ]
        )
    )
    tester.run("pyroscope-cluster-relation-created")
    tester.assert_relation_data_empty()


def test_validation_succeeds_on_joining_with_role():
    tester = Tester(
        state_in=State(
            relations=[
                Relation(
                    endpoint="pyroscope_cluster",
                    interface="pyroscope_cluster",
                    remote_app_name="worker",
                    remote_app_data={
                        "role": json.dumps("all"),
                    },
                    remote_units_data={
                        0: {
                            "juju_topology": json.dumps(
                                {
                                    "application": "worker",
                                    "unit": "worker/0",
                                    "charm_name": "worker",
                                }
                            ),
                            "address": json.dumps("192.0.2.1"),
                        }
                    },
                ),
            ]
        )
    )
    tester.run("pyroscope-cluster-relation-joined")
    tester.assert_schema_valid()


def test_validation_fails_on_joining_with_invalid_role():
    tester = Tester(
        state_in=State(
            relations=[
                Relation(
                    endpoint="pyroscope_cluster",
                    interface="pyroscope_cluster",
                    remote_app_name="worker",
                    remote_app_data={"role": json.dumps("imposter")},
                    remote_units_data={
                        0: {
                            "juju_topology": json.dumps(
                                {
                                    "application": "worker",
                                    "unit": "worker/0",
                                    "charm_name": "worker",
                                }
                            ),
                            "address": json.dumps("192.0.2.1"),
                        }
                    },
                )
            ]
        )
    )
    tester.run("pyroscope-cluster-relation-joined")
    tester.assert_relation_data_empty()
