# Copyright 2025 Canonical
# See LICENSE file for licensing details.

from interface_tester import Tester
from scenario import State, Relation


def test_add_content_on_relation_created():
    # GIVEN that the remote end has not published any tables
    t = Tester(
        State(
            leader=True,
            relations=[
                Relation(
                    endpoint="etcd-client",
                    interface="etcd_client",
                )
            ],
        )
    )
    # WHEN the database charm receives a relation-joined event
    state_out = t.run("etcd-client-relation-joined")
    # THEN no data is published to the (local) databags
    t.assert_schema_valid()
