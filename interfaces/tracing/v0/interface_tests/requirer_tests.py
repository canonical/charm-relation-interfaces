# Copyright 2023 Canonical
# See LICENSE file for licensing details.
import yaml

from interface_tester.interface_test import interface_test_case, SchemaConfig
from scenario import State, Relation


@interface_test_case(
    event='tracing-relation-created',
    role='requirer',
)
def test_no_data_on_created(output_state: State):
    return


@interface_test_case(
    event='tracing-relation-joined',
    role='requirer',
)
def test_no_data_on_joined(output_state: State):
    return


@interface_test_case(
    event='tracing-relation-changed',
    role='requirer',
    input_state=State(
        relations=[Relation(
            endpoint='tracing',
            interface='tracing',
            remote_app_name='remote',
        )]
    )
)
def test_data_published_on_changed_remote_valid(output_state: State):
    return


@interface_test_case(
    event='tracing-relation-changed',
    role='requirer',
    input_state=State(relations=[Relation(
        endpoint='tracing',
        interface='tracing',
        remote_app_name='remote',
    )]
    ),
)
def test_data_published_on_changed_remote_invalid(output_state: State):
    return
