from scenario import State, Relation, PeerRelation
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

