# Copyright 2023 Canonical
# See LICENSE file for licensing details.
import json

from interface_tester.interface_test import interface_test_case, SchemaConfig
from scenario import State, Relation


@interface_test_case(
    event='tracing-relation-created',
    role='provider',
    schema=SchemaConfig.empty
)
def test_no_data_on_created(output_state: State):
    return


@interface_test_case(
    event='tracing-relation-joined',
    role='provider',
    schema=SchemaConfig.empty
)
def test_no_data_on_joined(output_state: State):
    return


@interface_test_case(
    event='tracing-relation-changed',
    role='provider',
    input_state=State(
        relations=[Relation(
            endpoint='tracing',
            interface='tracing',
            remote_app_name='remote',
            local_app_data={
                "host": "foo.com",
                "ingesters": json.dumps([
                    {"protocol": "otlp_grpc",
                     "port": "4242"}
                ])
            }
        )]
    )
)
def test_data_on_changed(output_state: State):
    return
