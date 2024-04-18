# Copyright 2024 Canonical
# See LICENSE file for licensing details.

from interface_tester import Tester
from scenario import Relation, State


def test_state_active_on_joined():
    t = Tester(
        State(
            relations=[
                Relation(
                    endpoint="sdcore_config",
                    interface="sdcore_config",
                )
            ],
        )
    )
    state_out: State = t.run('sdcore-config-relation-joined')
    assert state_out.unit_status.name == 'active'


def test_state_blocked_on_broken():
    t = Tester(
        State(
            relations=[
                Relation(
                    endpoint="sdcore_config",
                    interface="sdcore_config",
                )
            ],
        )
    )
    state_out: State = t.run('sdcore-config-relation-broken')
    assert state_out.unit_status.name == 'blocked'


