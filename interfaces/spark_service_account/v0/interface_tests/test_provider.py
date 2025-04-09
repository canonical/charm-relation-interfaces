from interface_tester import Tester
from scenario import State, Relation


def test_nothing_happens_if_remote_empty():
    # GIVEN that the remote end has not published anything on databag
    t = Tester(
        State(
            leader=True,
            relations=[
                Relation(
                    endpoint="spark-service-account",
                    interface="spark_service_account",
                )
            ],
        )
    )

    # WHEN this charm receives a relation-joined event
    state_out = t.run("spark-service-account-relation-joined")

    # THEN no data is published to the (local) databags
    t.assert_relation_data_empty()


def test_data_written_happy_path():
    # GIVEN that the remote end has requested a service account in the right format
    t = Tester(
        State(
            leader=True,
            relations=[
                Relation(
                    endpoint="spark-service-account",
                    interface="spark_service_account",
                    remote_app_data={"service-account": "namespace:sa-name"},
                )
            ],
        )
    )
    # WHEN this charm receives a relation-changed event
    state_out = t.run("spark-service-account-relation-changed")

    # THEN the schema is satisfied (this charm published all required fields)
    t.assert_schema_valid()
