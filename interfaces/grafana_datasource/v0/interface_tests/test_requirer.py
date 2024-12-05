from interface_tester import Tester
from scenario import State, Relation
import json


def test_nothing_happens_on_no_remote_data():
    # GIVEN the remote side hasn't shared their datasource endpoint yet
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
    # WHEN the requirer processes a relation-joined event
    tester.run('grafana-source-relation-joined')
    # THEN nothing is written to the databags
    tester.assert_relation_data_empty()


def test_nothing_happens_on_invalid_remote_data():
    # GIVEN the remote side has shared gibberish
    tester = Tester(state_in=State(
        relations=[
            Relation(
                endpoint='grafana-source',
                interface='grafana_datasource',
                remote_app_name='foo',
                remote_app_data={"foo": "bar"},
                remote_units_data={
                    0: {"baz": "qux"}
                }
            )
        ]
    ))
    # WHEN the requirer processes a relation-changed event
    tester.run('grafana-source-relation-changed')
    # THEN nothing is written to the databags
    tester.assert_relation_data_empty()


def test_datasource_uid_shared_if_remote_data_valid():
    # GIVEN the remote side has shared a valid datasource endpoint
    relation_in = Relation(endpoint='grafana-source',
                           interface='grafana_datasource',
                           remote_app_name='foo',
                        remote_app_data={"grafana_source_data": json.dumps(
                            {"model": "somemodel", "model_uuid": "0000-0000-0000-0042", "application": "myapp",
                             "type": "prometheus", })},
                           remote_units_data={
                               0: {"grafana_source_host": "somehost:80"},
                               42: {"grafana_source_host": "someotherhost:80"},
                           })
    tester = Tester(state_in=State(
        relations=[
            relation_in
        ]
    ))

    # WHEN the requirer processes a relation-changed event
    state_out = tester.run('grafana-source-relation-changed')

    # THEN the schema is valid
    tester.assert_schema_valid()

    # AND THEN the requirer has shared a datasource UID
    rel_out = [r for r in state_out.relations if r.id == relation_in.id][0]
    ds_uids = json.loads(rel_out.local_app_data['datasource_uids'])

    # each requirer unit has received a datasource uid
    assert ds_uids['foo/0']
    assert ds_uids['foo/42']
