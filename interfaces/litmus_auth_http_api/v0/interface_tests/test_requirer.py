import json

from interface_tester import Tester
from scenario import State, Relation


def test_data_on_created_remote_empty():
    # on created: the requirer does nothing if the provider hasn't done its part
    t = Tester(
        State(leader=True,
              relations=[
                  Relation(
                      endpoint="http-api",
                      interface="litmus_auth_http_api",
                  )
              ]
          )
    )
    t.run("http-api-relation-created")
    t.assert_relation_data_empty()


def test_data_on_joined_remote_empty():
    # on joined: the requirer does nothing if the provider hasn't done its part
    t = Tester(
        State(leader=True,
              relations=[
                  Relation(
                      endpoint="http-api",
                      interface="litmus_auth_http_api",
                  )
              ]
          )
    )
    t.run("http-api-relation-joined")
    t.assert_relation_data_empty()


def test_data_on_changed_remote_empty():
    # on changed: the requirer does nothing if the provider hasn't done its part
    t = Tester(
        State(leader=True,
              relations=[
                  Relation(
                      endpoint="http-api",
                      interface="litmus_auth_http_api",
                  )
              ]
          )
    )
    t.run("http-api-relation-changed")
    t.assert_relation_data_empty()


def test_data_on_changed():
    # on changed: if the provider publishes its side of the data, we do our part (which is almost nothing)
    t = Tester(
        State(leader=True,
              relations=[
                  Relation(
                      endpoint="http-api",
                      interface="litmus_auth_http_api",
                      remote_app_data={
                          "endpoint": json.dumps("http://foo.com:2025/"),
                          "version": "0"
                      }
                  )
              ]
          )
    )
    t.run("http-api-relation-changed")
    t.assert_schema_valid()
