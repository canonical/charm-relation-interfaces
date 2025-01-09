# Copyright 2024 Canonical
# See LICENSE file for licensing details.
import json

from interface_tester.interface_test import Tester
from scenario import State, Relation

_VALID_REQUIRER_APP_DATA = {"receivers": json.dumps(
    [
        {
            "protocol": {
                "name": "otlp_grpc",
                "type": "grpc"
            },
            "url": "http://192.0.2.0/24"
        }
    ]
)
}


def test_data_on_created():
    tester = Tester(
        state_in=State(
            relations=[
                Relation(
                    endpoint='tracing',
                    interface='tracing',
                    remote_app_name='remote',
                    remote_app_data=_VALID_REQUIRER_APP_DATA
                )
            ]
        )
    )
    tester.run('tracing-relation-created')
    tester.assert_schema_valid()


def test_data_on_joined():
    tester = Tester(
        state_in=State(
            relations=[
                Relation(
                    endpoint='tracing',
                    interface='tracing',
                    remote_app_name='remote',
                    remote_app_data=_VALID_REQUIRER_APP_DATA                )
            ]
        )
    )
    tester.run('tracing-relation-joined')
    tester.assert_schema_valid()


def test_data_on_changed():
    tester = Tester(
        state_in=State(
            relations=[
                Relation(
                    endpoint='tracing',
                    interface='tracing',
                    remote_app_name='remote',
                    remote_app_data=_VALID_REQUIRER_APP_DATA                )
            ]
        )
    )
    tester.run('tracing-relation-changed')
    tester.assert_schema_valid()
