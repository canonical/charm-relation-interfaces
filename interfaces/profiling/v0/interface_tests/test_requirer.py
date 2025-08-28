# Copyright 2024 Canonical
# See LICENSE file for licensing details.
import json

from interface_tester.interface_test import Tester
from scenario import State, Relation

# on created, joined, changed: the requirer is expected to publish no data
def test_no_data_on_created():
    tester = Tester()
    tester.run('tracing-relation-created')
    tester.assert_relation_data_empty()


def test_no_data_on_joined():
    tester = Tester()
    tester.run('tracing-relation-joined')
    tester.assert_relation_data_empty()


def test_no_data_on_changed():
    tester = Tester()
    tester.run('tracing-relation-changed')
    tester.assert_relation_data_empty()


# if the remote end has sent their side of the deal, we're happy
def test_data_on_changed():
    tester = Tester(
        state_in=State(
            relations=[
                Relation(
                    endpoint='profiling',
                    interface='profiling',
                    remote_app_name='remote',
                    remote_app_data={
                        "otlp_grpc_endpoint_url": json.dumps("my.fqdn.cluster.local:1234"),
                        "insecure": json.dumps(False),
                    }
                    )
            ]
        )
    )
    tester.run('tracing-relation-changed')
    tester.assert_schema_valid()

