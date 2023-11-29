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
        # config={
        #     "entity_id": "https://login.staging.ubuntu.com",
        #     "metadata_url": "https://login.staging.ubuntu.com/saml/metadata"
        # },
    ))
    t.run("saml-relation-created")
    t.assert_schema_valid()
