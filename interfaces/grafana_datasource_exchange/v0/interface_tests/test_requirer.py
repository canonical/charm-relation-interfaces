from interface_tester import Tester
from scenario import State, Relation


def test_datasource_exchange():
    # GIVEN the grafana_datasource interface has shared one or more source UIDs
    source_exchange = Relation(
        endpoint='grafana-source-exchange',
        interface='grafana_datasource_exchange',
        remote_app_name='bar'
    )
    tester = Tester(state_in=State(
        relations=[
            source_exchange
        ]
    ))
    # WHEN the requirer processes any relation event
    tester.run('grafana-source-exchange-relation-changed')
    # THEN the requirer publishes valid data
    tester.assert_schema_valid()
