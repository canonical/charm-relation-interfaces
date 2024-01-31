# Copyright 2023 Canonical
# See LICENSE file for licensing details.
import json
from typing import List, Any

from interface_tester import DataBagSchema
from interface_tester.interface_test import Tester
from pydantic import BaseModel, Json
from scenario import State, Relation


class LegacyTracingProviderData(BaseModel):
    host: str
    ingesters: Json[List[Any]]


class LegacyProviderSchema(DataBagSchema):
    """Provider schema for Tracing."""
    app: LegacyTracingProviderData


def test_legacy_response_on_created_no_data():
    tester = Tester()
    tester.run('tracing-relation-created')
    tester.assert_schema_valid(LegacyProviderSchema)


def test_legacy_response_on_joined_no_data():
    tester = Tester()
    tester.run('tracing-relation-joined')
    tester.assert_schema_valid(LegacyProviderSchema)


def test_legacy_response_on_changed_no_data():
    tester = Tester()
    tester.run('tracing-relation-changed')
    tester.assert_schema_valid(LegacyProviderSchema)


def test_no_response_on_bad_data():
    tester = Tester(state_in=State(relations=[
        Relation(
            endpoint='tracing',
            interface='tracing',
            remote_app_data={"bubble": "rubble"}
        )
    ]))
    tester.run('tracing-relation-changed')
    tester.assert_relation_data_empty()


def test_data_on_created():
    tester = Tester(
        state_in=State(
            relations=[
                Relation(
                    endpoint='tracing',
                    interface='tracing',
                    remote_app_name='remote',
                    remote_app_data={
                        "receivers": json.dumps(["otlp_grpc", "tempo_http", "tempo_grpc"])
                    }
                )
            ]
        )
    )
    tester.run('tracing-relation-created')
    tester.assert_schema_valid()


def test_data_on_joined():
    tester = Tester(
        state_in=State(
            relations=[
                Relation(
                    endpoint='tracing',
                    interface='tracing',
                    remote_app_name='remote',
                    remote_app_data={
                        "receivers": json.dumps(["otlp_grpc", "tempo_http", "tempo_grpc"])
                    }
                )
            ]
        )
    )
    tester.run('tracing-relation-joined')
    tester.assert_schema_valid()


def test_data_on_changed():
    tester = Tester(
        state_in=State(
            relations=[
                Relation(
                    endpoint='tracing',
                    interface='tracing',
                    remote_app_name='remote',
                    remote_app_data={
                        "receivers": json.dumps(["otlp_grpc", "tempo_http", "tempo_grpc"])
                    }
                )
            ]
        )
    )
    tester.run('tracing-relation-changed')
    tester.assert_schema_valid()
