# Copyright 2023 Canonical
# See LICENSE file for licensing details.

from interface_tester.interface_test import interface_test_case, SchemaConfig
from scenario import State, Relation


@interface_test_case(
    event='ingress-relation-created',
    role='provider',
    schema=SchemaConfig.empty
)
def test_no_data_on_created(output_state: State):
    # nothing happens on created: databags are empty
    return


@interface_test_case(
    event='ingress-relation-joined',
    role='provider',
    schema=SchemaConfig.empty
)
def test_no_data_on_joined(output_state: State):
    # nothing happens on joined: databags are empty
    return


@interface_test_case(
    event='ingress-relation-changed',
    role='provider',
    input_state=State(
        relations=[Relation(
            endpoint='ingress',
            interface='ingress',
            remote_app_name='remote',
            remote_app_data={
                'model': '"bar"',
                'port': '42',
                'name': '"remote"',
            },
            remote_units_data={
                0:
                    {
                        'host': '"0.0.0.42"',
                    }
            }
        )]
    )
)
def test_data_published_on_changed_remote_valid(output_state: State):
    return  # schema validation is enough for now


@interface_test_case(
    event='ingress-relation-changed',
    role='provider',
    input_state=State(
        relations=[Relation(
            endpoint='ingress',
            interface='ingress',
            remote_app_name='remote',
            remote_app_data={
                'model': 'bar',
                'port': '42',
                'name': 'true',
            },
            remote_units_data={
                0:
                    {
                        'host': '0.0.0.42',
                    }
            }
        )]
    ),
    schema=SchemaConfig.empty
)
def test_data_published_on_changed_remote_invalid_json(output_state: State):
    # on changed, if the remote side has sent invalid json: local side didn't publish anything either.
    return


@interface_test_case(
    event='ingress-relation-changed',
    role='provider',
    input_state=State(relations=[Relation(
        endpoint='ingress',
        interface='ingress',
        remote_app_name='remote',
        remote_app_data={
            'port': '42',
            'bubble': 'rubble'
        }
    )]
    ),
    schema=SchemaConfig.empty
)
def test_data_published_on_changed_remote_invalid(output_state: State):
    # on changed, if the remote side has sent INvalid data: local side didn't publish anything either.
    return
