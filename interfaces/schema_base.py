"""This module contains base python classes used by interface schemas."""

from pydantic import BaseModel
from typing import Optional


class DataBagSchema(BaseModel):
    """Base class for relation interface databag schemas.

    Subclass from this base class and override "unit" and/or "app" to create a specification for
    a databag schema.

    For example:

    >>> from pydantic import Json
    >>>
    >>> class MyUnitRequirerSchema(DataBagSchema):
    >>>     foo: Json[int]
    >>>     bar: str
    >>>
    >>> # this class needs to be named "RequirerSchema"
    >>> # for it to be picked up by the automated tester.
    >>> class RequirerSchema(DataBagSchema):
    >>>     unit: MyUnitRequirerSchema
    >>>     # you can omit `unit` or `app` if the databag is expected to be empty.
    >>>
    >>> # you can also omit either `RequirerSchema` or `ProviderSchema` altogether if the requirer
    >>> # or the provider, respectively, do not expose any relation data.
    >>>
    >>> # class ProviderSchema(DataBagSchema):
    >>>     # ...


    This specifies that for a relation to satisfy MyRequirerSchema, the application databag
    needs to be empty and the unit databag needs to contain exactly a "bar":string and a
    "foo":Json-encoded int value.

    By using pydantic's validator API, you can specify further constraints on the values,
    provide defaults, enforce encoding/decoding, and more.
    """
    unit: Optional[BaseModel] = None
    app: Optional[BaseModel] = None
