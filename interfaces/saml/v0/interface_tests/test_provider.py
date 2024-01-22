# Copyright 2023 Canonical
# See LICENSE file for licensing details.
from interface_tester.interface_test import Tester
from scenario import Relation, State


def test_data_published_on_created():
    t = Tester(State(
        relations=[Relation(
            endpoint="saml",
            interface="saml",
        )],
    ))
    t.run("saml-relation-created")
    t.assert_schema_valid()
