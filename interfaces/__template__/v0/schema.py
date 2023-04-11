"""This file defines the schemas for the provider and consumer sides of this relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- ConsumerSchema
"""

from interfaces.schema_base import DataBagSchema


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of this interface."""


class ConsumerSchema(DataBagSchema):
    """The schema for the consumer side of this interface."""
