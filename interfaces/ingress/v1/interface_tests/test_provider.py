# Copyright 2023 Canonical
# See LICENSE file for licensing details.
import yaml

from interface_tester import Tester
from scenario import State, Relation
from scenario.context import CharmEvents


def test_no_data_on_created():
    t = Tester(
        State(leader=True,
            relations=[
                Relation(
                    endpoint="ingress",
                    interface="ingress",
                )
            ]
        )
    )
    state_out = t.run("ingress-relation-created")
    t.assert_relation_data_empty()


def test_no_data_on_joined():
    # nothing happens on joined: databags are empty
    t = Tester(
        State(leader=True,
            relations=[
                Relation(
                    endpoint="ingress",
                    interface="ingress",
                )
            ]
        )
    )
    state_out = t.run("ingress-relation-joined")
    t.assert_relation_data_empty()


def test_data_published_on_changed_remote_valid():
    ingress = Relation(
        endpoint='ingress', interface='ingress',
        remote_app_data={'host': '"0.0.0.42"', 'model': '"bar"', 'name': '"remote/0"', 'port': '42'}
    )
    t = Tester(State(leader=True, relations=[ingress]))
    state_out = t.run(CharmEvents.relation_changed(ingress))
    t.assert_schema_valid()


def test_no_data_published_on_changed_remote_invalid():
    # on changed, if the remote side has sent INvalid data: local side didn't publish anything either.
    t = Tester(
        State(leader=True,
              relations=[Relation(
                  endpoint='ingress',
                  interface='ingress',
                  remote_app_data={
                      'host': '0.0.0.42',
                      'bubble': "10",
                      'rubble': "foo"
                  }
              )]
              )
    )
    state_out = t.run("ingress-relation-changed")
    t.assert_relation_data_empty()
