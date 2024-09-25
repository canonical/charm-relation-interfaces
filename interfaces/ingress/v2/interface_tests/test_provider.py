# Copyright 2024 Canonical
# See LICENSE file for licensing details.

import scenario
from interface_tester import Tester


def test_no_data_on_created():
    # nothing happens on created: databags are empty
    t = Tester(
        scenario.State(
            leader=True,
            relations=[
                scenario.Relation(
                    endpoint="ingress",
                    interface="ingress",
                )
            ],
        )
    )
    state_out = t.run("ingress-relation-created")
    t.assert_relation_data_empty()


def test_no_data_on_joined():
    # nothing happens on joined: databags are empty
    t = Tester(
        scenario.State(
            leader=True,
            relations=[
                scenario.Relation(
                    endpoint="ingress",
                    interface="ingress",
                )
            ],
        )
    )
    state_out = t.run("ingress-relation-joined")
    t.assert_relation_data_empty()


def test_data_published_on_changed_remote_valid():
    relation = scenario.Relation(
        endpoint="ingress",
        interface="ingress",
        remote_app_name="remote",
        remote_app_data={
            "model": '"bar"',
            "port": "42",
            "name": '"remote"',
        },
        remote_units_data={
            0: {
                "host": '"0.0.0.42"',
            }
        },
    )
    t = Tester(scenario.State(relations=[relation]))
    state_out = t.run(scenario.context.CharmEvents.relation_changed(relation))
    t.assert_schema_valid()


def test_data_published_on_changed_remote_invalid_json():
    # on changed, if the remote side has sent invalid json: local side didn't publish anything either.
    ingress = scenario.Relation(
        endpoint="ingress",
        interface="ingress",
        remote_app_data={
            "model": "bar",
            "port": "42",
            "name": "true",
        },
        remote_units_data={
            0: {
                "host": "0.0.0.42",
            }
        },
    )
    t = Tester(scenario.State(leader=True, relations=[ingress]))
    state_out = t.run(scenario.context.CharmEvents.relation_changed(ingress))
    t.assert_relation_data_empty()


def test_data_published_on_changed_remote_invalid():
    # on changed, if the remote side has sent invalid data: local side didn't publish anything either.
    ingress = scenario.Relation(
        endpoint="ingress",
        interface="ingress",
        remote_app_data={"model": '"bar"', "port": "42", "name": '"true"'},
        remote_units_data={
            0: {
                "bubble": "blabla",
            }
        },
    )
    t = Tester(scenario.State(leader=True, relations=[ingress]))
    state_out = t.run(scenario.context.CharmEvents.relation_changed(ingress))
    t.assert_relation_data_empty()
