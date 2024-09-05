from scenario import Secret, State, Relation, PeerRelation
from interface_tester import Tester


# def test_no_data_on_created():
#     t = Tester(
#         State(
#             leader=True,
#             relations=[Relation(endpoint="zookeeper", interface="zookeeper")],
#         )
#     )
#     t.run("database-relation-created")
#     t.assert_relation_data_empty()


# def test_no_data_on_joined():
#     t = Tester(
#         State(
#             leader=True,
#             relations=[
#                 Relation(
#                     endpoint="zookeeper",
#                     interface="zookeeper",
#                 )
#             ],
#         )
#     )
#     t.run("database-relation-joined")
#     t.assert_relation_data_empty()


# def test_database_requested():
#     t = Tester(
#         State(
#             leader=True,
#             relations=[
#                 Relation(
#                     endpoint="zookeeper",
#                     interface="zookeeper",
#                     remote_app_data={
#                         "database": "lotr",
#                         "requested-secrets": '["username","password","tls","tls-ca","uris"]',
#                     },
#                 )
#             ],
#         )
#     )
#     state = t.run("zookeeper-relation-changed")
#     t.assert_relation_data_empty()


def test_database_creds_in_secrets():
    secrets = [
        Secret(
            id="secret:20171337734412181011",
            contents={0: {"relation-1": "speakfriend"}},
            owner="app",
            revision=0,
            remote_grants={},
            label="cluster.zookeeper-k8s.app",
            description=None,
            expire=None,
            rotate=None,
        )
    ]

    cluster_peer = PeerRelation(
        "cluster", "cluster", local_app_data={str(i): "added" for i in range(4)}
    )
    t = Tester(
        State(
            leader=True,
            relations=[
                cluster_peer,
                Relation(
                    endpoint="zookeeper",
                    interface="zookeeper",
                    remote_app_data={
                        "database": "lotr",
                        "requested-secrets": '["username","password","tls","tls-ca","uris"]',
                    },
                ),
            ],
            secrets=secrets,
        )
    )
    state = t.run("cluster-relation-changed")
    t.assert_schema_valid()
