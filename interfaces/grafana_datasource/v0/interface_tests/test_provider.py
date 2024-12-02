from interface_tester import Tester
from scenario import State, Relation


def test_share_datasource_on_remote_joined():
    # GIVEN the remote side hasn't sent anything
    tester = Tester(state_in=State(
        relations=[
            Relation(
                endpoint='grafana-source',
                interface='grafana_datasource',
                remote_app_name='foo',
                remote_app_data={},
                remote_units_data={
                    0: {}
                }
            )
        ]
    ))
    # WHEN the provider processes a relation-joined event
    tester.run('grafana-source-relation-joined')
    # THEN the provider publishes valid datasource data
    tester.assert_schema_valid()

