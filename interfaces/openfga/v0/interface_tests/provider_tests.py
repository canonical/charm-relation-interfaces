# Copyright 2023 Canonical
# See LICENSE file for licensing details.
import yaml
from interface_tester.interface_test import SchemaConfig, interface_test_case
from scenario import Relation, State


@interface_test_case(
    event='openfga-relation-created',
    role='provider',
    schema=SchemaConfig.empty
)
def test_no_data_on_created(output_state: State):
    # nothing happens on created: databags are empty
    return


@interface_test_case(
    event='openfga-relation-joined',
    role='provider',
    schema=SchemaConfig.empty
)
def test_no_data_on_joined(output_state: State):
    # nothing happens on joined: databags are empty
    return


@interface_test_case(
    event='openfga-relation-changed',
    role='provider',
    input_state=State(
        relations=[Relation(
            endpoint='openfga',
            interface='openfga',
            remote_app_name='remote',
            remote_app_data={
                'store_name': 'test-store'
            }
        )]
    )
)
def test_data_published_on_changed_remote_valid(output_state: State):
    return  # schema validation is enough for now
