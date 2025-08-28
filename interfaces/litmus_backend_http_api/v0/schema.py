"""This file defines the schemas for the provider and requirer sides of this relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""
import pydantic
from interface_tester.schema_base import DataBagSchema


class VersionedAppDatabagSchema(pydantic.BaseModel):
    version: pydantic.Json[int] = pydantic.Field(
        description="Version of the schema being used by the endpoint wrapper. Json-encoded.",
        examples=["0", "1"]
    )

class ProviderAppDatabagSchema(VersionedAppDatabagSchema):
    endpoint: pydantic.Json[pydantic.HttpUrl] = pydantic.Field(
        description="URL of an http(s) endpoint serving a litmus backend. Json-encoded.",
        examples=["'http://192.0.2.0:2020/'", "'https://foo.com/'"]
    )


class RequirerAppDatabagSchema(VersionedAppDatabagSchema):
    endpoint: pydantic.Json[pydantic.HttpUrl] = pydantic.Field(
        description="URL of an http(s) endpoint serving a litmus frontend. Json-encoded.",
        examples=["'http://192.0.2.0:2020/'", "'https://foo.com/'"]
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""
    app: ProviderAppDatabagSchema


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""
    app: RequirerAppDatabagSchema