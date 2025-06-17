from interface_tester import Tester
from scenario import Relation, State


def test_requirer_happy_path():
    relation_data = {
        "connector_charm_name": "opencti-connector-charm",
        "connector_type": "EXTERNAL_IMPORT",
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
