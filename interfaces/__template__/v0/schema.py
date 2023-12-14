"""This file defines the schemas for the provider and requirer sides of this relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from interface_tester.schema_base import DataBagSchema


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of this interface."""
