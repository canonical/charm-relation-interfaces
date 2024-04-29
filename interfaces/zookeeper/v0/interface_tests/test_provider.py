from scenario import State, Relation
from interface_tester import Tester


def test_no_data_on_created():
    t = Tester(
        State(
            leader=True,
            relations=[Relation(endpoint="database", interface="zookeeper")],
        )
    )
    t.run("database-relation-created")
    t.assert_relation_data_empty()


def test_no_data_on_joined():
    t = Tester(
        State(
            leader=True,
            relations=[
                Relation(
                    endpoint="database",
                    interface="zookeeper",
                )
            ],
        )
    )
    t.run("database-relation-joined")
    t.assert_relation_data_empty()


def test_data_published_on_changed_remote_valid():
    zk = Relation(
        endpoint="database",
        interface="zookeeper",
        remote_app_data={
            "database": "/myapp",
            "requested-secrets": """["username","password","tls","tls-ca","uris"]""",
        },
    )
    t = Tester(State(leader=True, relations=[zk]))
    t.run(zk.changed_event)
    # t.run("config-changed")
    t.assert_schema_valid()
