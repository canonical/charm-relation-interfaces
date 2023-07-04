# Copyright 2023 Canonical
# See LICENSE file for licensing details.
import yaml
from interface_tester.interface_test import SchemaConfig, interface_test_case
from scenario import Relation, State


@interface_test_case(
    event='openfga-relation-created',
    role='requirer',
    schema=SchemaConfig.empty
)
def test_no_data_on_created(output_state: State):
    # nothing happens on created: databags are empty
    return


@interface_test_case(
    event='openfga-relation-joined',
    role='requirer',
    schema=SchemaConfig.empty
)
def test_no_data_on_joined(output_state: State):
    # nothing happens on joined: databags are empty
    return


@interface_test_case(
    event='openfga-relation-changed',
    role='requirer',
    input_state=State(
        relations=[Relation(
            endpoint='openfga',
            interface='openfga',
            remote_app_name='remote',
            remote_app_data={
                'address': '10.10.4.1',
                'port': "8080",
                'scheme': 'https',
                'token_secret_id': "test_token_secret",
                'store_id': '01GK13VYZK62Q1T0X55Q2BHYD6',
            }
        )]
    )
)
def test_data_published_on_changed_remote_valid(output_state: State):
    return  # schema validation is enough for now
