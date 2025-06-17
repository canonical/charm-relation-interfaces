from interface_tester import Tester
from scenario import Relation, State


def test_provider_happy_path():
    relation_data = {
        "opencti_url": "http://opencti-endpoints.stg-opencti.svc:8080",
        "opencti_token": "secret:secret-id",
    }
    t = Tester(
        State(
            leader=True,
            relations=[
                Relation(
                    endpoint="opencti-connector",
                    interface="opencti_connector",
                    remote_app_data=relation_data,
                )
            ],
        )
    )
    t.run("opencti-connector-relation-changed")
    t.assert_schema_valid()
