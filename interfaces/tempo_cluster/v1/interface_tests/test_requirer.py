# Copyright 2024 Canonical
# See LICENSE file for licensing details.

from interface_tester.interface_test import Tester
from scenario import State, Relation
import json


def test_data_on_created():
    tester = Tester(state_in=State(
        relations=[
            Relation(
                endpoint='tempo_cluster',
                interface='tempo_cluster',
                remote_app_name='coordinator',
                remote_app_data={
                    "worker_config": json.dumps("foo: bar")
                },
                charm_tracing_receivers={
                    "otlp_http": "http://1.2.3.4:4318",
                },
                workload_tracing_receivers={
                    "otlp_http": "http://5.6.7.8:4318",
                    "otlp_grpc": "5.6.7.8:4317",
                },
            )
        ]
    ))
    tester.run('tempo-cluster-relation-created')
    tester.assert_schema_valid()
