# Copyright 2025 Canonical
# See LICENSE file for licensing details.
import json

from interface_tester.interface_test import Tester
from scenario import Relation, State


def test_validation_succeeds_on_joining_with_endpoint():
    tester = Tester(
        state_in=State(
            relations=[
                Relation(
                    endpoint="litmus_auth",
                    interface="litmus_auth",
                    remote_app_name="backend",
                    remote_app_data={
                        "grpc_server_host": json.dumps("192.0.2.1"),
                        "grpc_server_port": json.dumps(8080),
                        "insecure": json.dumps(False),
                        "version": json.dumps(0),
                    },
                ),
            ]
        )
    )
    tester.run("litmus-auth-relation-joined")
    tester.assert_schema_valid()
