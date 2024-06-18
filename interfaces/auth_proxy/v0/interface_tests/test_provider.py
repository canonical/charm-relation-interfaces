# Copyright 2024 Canonical
# See LICENSE file for licensing details.

from interface_tester import Tester
from scenario import State, Relation
import json


def test_nothing_happens_if_remote_empty():
    # given that the remote end has not published any data
    t = Tester(
        State(
            leader=True,
            relations=[
                Relation(
                    endpoint="auth-proxy",  # the name doesn't matter
                    interface="auth_proxy",
                )
            ],
        )
    )
    # when the charm receives a relation-joined event
    state_out = t.run("auth-proxy-relation-joined")
    # no data is published to the (local) databags
    t.assert_relation_data_empty()


# def test_contract_happy_path():
#     # given that the remote end has requested tables in the right format
#     t = Tester(
#         State(
#             leader=True,
#             relations=[
#                 Relation(
#                     endpoint="auth-proxy",  # the name doesn't matter
#                     interface="auth_proxy",
#                     remote_app_data={
#                         "providers": json.dumps(["protected_urls", "allowed_endpoints", "headers"])
#                     },
#                 )
#             ],
#         )
#     )
#     # when the charm receives a relation-changed event
#     state_out = t.run("auth-proxy-relation-changed")
#     # THEN the schema is satisfied (the database charm published all required fields)
#     t.assert_schema_valid()
