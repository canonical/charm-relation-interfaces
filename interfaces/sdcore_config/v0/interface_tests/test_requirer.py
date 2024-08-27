# Copyright 2024 Canonical
# See LICENSE file for licensing details.

from interface_tester import Tester
from scenario import Relation, State


def test_no_data_on_joined():
    t = Tester(
        State(
            relations=[
                Relation(
                    endpoint="sdcore_config",
                    interface="sdcore_config",
                    remote_app_data={"webui_url": "some_url:123"},
                )
            ],
        )
    )
    t.run('sdcore-config-relation-joined')
    t.assert_relation_data_empty()
