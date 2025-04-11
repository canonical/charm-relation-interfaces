# Copyright 2025 Canonical
# See LICENSE file for licensing details.

from interface_tester import Tester
from scenario import Secret, State, Relation


def test_nothing_happens_if_remote_empty():
    # GIVEN that the remote end has not published any tables
    t = Tester(
        State(
            leader=True,
            relations=[
                Relation(
                    endpoint="etcd-client",  # the name doesn't matter
                    interface="etcd_client",
                )
            ],
        )
    )
    # WHEN the database charm receives a relation-joined event
    state_out = t.run("etcd-client-relation-joined")
    # THEN no data is published to the (local) databags
    t.assert_relation_data_empty()


def test_add_provider_content():
    # GIVEN that the remote end has requested tables in the right format
    secret = Secret({"mtls-cert": "test_ca"}, owner="app")
    t = Tester(
        State(
            leader=True,
            relations=[
                Relation(
                    endpoint="etcd-client",  # the name doesn't matter
                    interface="etcd_client",
                    remote_app_data={
                        "prefix": "/my/keys",
                        "secret-mtls": secret.id,
                        "requested-secrets": ["username", "uris", "tls", "tls-ca"],
                        "provided-secrets": ["mtls-cert"],
                    },
                )
            ],
        )
    )
    # WHEN the database charm receives a relation-changed event
    state_out = t.run("etcd-client-relation-changed")
    # THEN the schema is satisfied (the database charm published all required fields)
    t.assert_schema_valid()
