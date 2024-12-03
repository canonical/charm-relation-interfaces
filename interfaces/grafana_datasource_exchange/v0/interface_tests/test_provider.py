import json

from interface_tester import Tester
from scenario import State, Relation


def test_not_share_partial_datasource():
    # GIVEN the grafana_datasource interface has not shared any source UID yet
    source = Relation(
        endpoint='grafana-source',
        interface='grafana_datasource',
        remote_app_name='foo',
        local_app_data={"grafana_source_data": json.dumps(
            {"model": "somemodel", "model_uuid": "0000-0000-0000-0042", "application": "myapp",
             "type": "prometheus", })},
        local_unit_data={"grafana_source_host": "somehost:80"},
        # no remote app data!
    )
    source_exchange = Relation(
        endpoint='grafana-source-exchange',
        interface='grafana_datasource_exchange',
        remote_app_name='bar'
    )
    tester = Tester(state_in=State(
        relations=[
            source,
            source_exchange
        ]
    ))
    # WHEN the provider processes any relation event
    tester.run('grafana-source-relation-changed')
    # THEN the provider publishes valid datasource-exchange data
    tester.assert_relation_data_empty()


def test_not_share_partial_datasource_remote_shared():
    # GIVEN the grafana_datasource interface has not shared any source UID yet
    source = Relation(
        endpoint='grafana-source',
        interface='grafana_datasource',
        remote_app_name='foo',
        local_app_data={"grafana_source_data": json.dumps(
            {"model": "somemodel", "model_uuid": "0000-0000-0000-0042", "application": "myapp",
             "type": "prometheus", })},
        local_unit_data={"grafana_source_host": "somehost:80"},
        # no remote app data!
    )
    # AND GIVEN the remote end of the source-exchange interface has shared some datasource UIDs already
    source_exchange = Relation(
        endpoint='grafana-source-exchange',
        interface='grafana_datasource_exchange',
        remote_app_name='bar',
        remote_app_data={"datasources": json.dumps([
            {
                "type": "tempo",
                "uid": "0000-0000-0000-0000"
            }
        ])}
    )
    tester = Tester(state_in=State(
        relations=[
            source,
            source_exchange
        ]
    ))
    # WHEN the provider processes any relation event
    tester.run('grafana-source-exchange-relation-changed')
    # THEN the provider doesn't share its side (as it doesn't have it yet)
    tester.assert_relation_data_empty()


def test_not_share_partial_datasource_remote_shared_invalid():
    # GIVEN the grafana_datasource interface has not shared any source UID yet
    source = Relation(
        endpoint='grafana-source',
        interface='grafana_datasource',
        remote_app_name='foo',
        local_app_data={"grafana_source_data": json.dumps(
            {"model": "somemodel", "model_uuid": "0000-0000-0000-0042", "application": "myapp",
             "type": "prometheus", })},
        local_unit_data={"grafana_source_host": "somehost:80"},
        # no remote app data!
    )
    # AND GIVEN the remote end of the source-exchange interface has shared some invalid data
    source_exchange = Relation(
        endpoint='grafana-source-exchange',
        interface='grafana_datasource_exchange',
        remote_app_name='bar',
        remote_app_data={"datasources": json.dumps([
            {
                "type": "tempo",
                "nope": "hope"
            }
        ])}
    )
    tester = Tester(state_in=State(
        relations=[
            source,
            source_exchange
        ]
    ))
    # WHEN the provider processes any relation event
    tester.run('grafana-source-exchange-relation-changed')
    # THEN the provider doesn't share its side (as it doesn't have it yet)
    tester.assert_relation_data_empty()


def test_datasource_exchange_remote_shared_invalid():
    # GIVEN the grafana_datasource interface has shared one or more sourdce UID
    source = Relation(
        endpoint='grafana-source',
        interface='grafana_datasource',
        remote_app_name='foo',
        local_app_data={"grafana_source_data": json.dumps(
            {"model": "somemodel", "model_uuid": "0000-0000-0000-0042", "application": "myapp",
             "type": "prometheus", })},
        local_unit_data={"grafana_source_host": "somehost:80"},
        remote_app_data={"datasource_uids": json.dumps({
            "foo/0": "myuid0",
            "foo/4": "myuid1"
        })}
    )
    # AND GIVEN the remote end of the source-exchange interface has shared some invalid data
    source_exchange = Relation(
        endpoint='grafana-source-exchange',
        interface='grafana_datasource_exchange',
        remote_app_name='bar',
        remote_app_data={"datasources": json.dumps([
            {
                "type": "tempo",
                "nope": "hope"
            }
        ])}
    )
    tester = Tester(state_in=State(
        relations=[
            source,
            source_exchange
        ]
    ))
    # WHEN the provider processes any relation event
    tester.run('grafana-source-exchange-relation-changed')
    # THEN the provider shares valid data even if the remote side is invalid
    tester.assert_schema_valid()


def test_datasource_exchange():
    # GIVEN the grafana_datasource interface has shared one or more sourdce UID
    source = Relation(
        endpoint='grafana-source',
        interface='grafana_datasource',
        remote_app_name='foo',
        local_app_data={"grafana_source_data": json.dumps(
            {"model": "somemodel", "model_uuid": "0000-0000-0000-0042", "application": "myapp",
             "type": "prometheus", })},
        local_unit_data={"grafana_source_host": "somehost:80"},
        remote_app_data={"datasource_uids": json.dumps({
            "foo/0": "myuid0",
            "foo/4": "myuid1"
        })}
    )
    source_exchange = Relation(
        endpoint='grafana-source-exchange',
        interface='grafana_datasource_exchange',
        remote_app_name='bar'
    )
    tester = Tester(state_in=State(
        relations=[
            source,
            source_exchange
        ]
    ))
    # WHEN the provider processes any relation event
    tester.run('grafana-source-relation-changed')
    # THEN the provider publishes valid datasource-exchange data
    tester.assert_schema_valid()
