from interface_tester import Tester
from scenario import State, Relation

def test_nothing_happens_if_remote_empty():
    # GIVEN that the remote end has not published anything on databag
    t = Tester(
        State(
            leader=True,
            relations=[
                Relation(
                    endpoint="azure-storage-credentials",
                    interface="azure_storage",
                )
            ],
        )
    )

    # WHEN this charm receives a relation-joined event
    state_out = t.run("azure-storage-credentials-relation-joined")

    # THEN no data is published to the (local) databags
    t.assert_relation_data_empty()


def test_data_written_happy_path():
    # GIVEN that the remote end has requested a container in the right format
    t = Tester(
        State(
            leader=True,
            relations=[
                Relation(
                    endpoint="azure-storage-credentials",
                    interface="azure_storage",
                    remote_app_data={"container": "my-container"},
                )
            ],
        )
    )
    # WHEN this charm receives a relation-changed event
    state_out = t.run("azure-storage-credentials-relation-changed")

    # THEN the schema is satisfied (this charm published all required fields)
    t.assert_schema_valid()