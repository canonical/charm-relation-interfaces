# Copyright 2023 Canonical
# See LICENSE file for licensing details.
import yaml
from interface_tester.interface_test import SchemaConfig, interface_test_case
from scenario import Relation, State


@interface_test_case(
    event='saml-relation-created',
    role='provider'
)
def test_data_published_on_created(output_state: State):
    return  # schema validation is enough for now

