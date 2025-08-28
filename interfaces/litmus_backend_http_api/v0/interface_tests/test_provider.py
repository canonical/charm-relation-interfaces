from interface_tester import Tester
from scenario import State, Relation


def test_data_on_created():
    # on created: the provider publishes its side of the data
    t = Tester(
        State(leader=True,
              relations=[
                  Relation(
                      endpoint="http-api",
                      interface="litmus_backend_http_api",
                  )
              ]
          )
    )
    t.run("http-api-relation-created")
    t.assert_schema_valid()


def test_data_on_joined():
    # on joined: the provider publishes its side of the data
    t = Tester(
        State(leader=True,
              relations=[
                  Relation(
                      endpoint="http-api",
                      interface="litmus_backend_http_api",
                  )
              ]
          )
    )
    t.run("http-api-relation-joined")
    t.assert_schema_valid()


def test_data_on_changed():
    # on changed: the provider publishes its side of the data
    t = Tester(
        State(leader=True,
              relations=[
                  Relation(
                      endpoint="http-api",
                      interface="litmus_backend_http_api",
                  )
              ]
          )
    )
    t.run("http-api-relation-changed")
    t.assert_schema_valid()
