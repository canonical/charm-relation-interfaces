# Copyright 2024 Canonical
# See LICENSE file for licensing details.

import json

from interface_tester.interface_test import Tester
from scenario import Relation, State


def test_data_on_created():
    tester = Tester(
        state_in=State(
            relations=[
                Relation(
                    endpoint="tempo_cluster",
                    interface="tempo_cluster",
                    remote_app_name="coordinator",
                    remote_app_data={"worker_config": json.dumps("foo: bar")},
                )
            ]
        )
    )
    tester.run("tempo-cluster-relation-created")
    tester.assert_schema_valid()
