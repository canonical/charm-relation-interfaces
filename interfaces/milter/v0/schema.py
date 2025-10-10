# Copyright 2023 Canonical
# See LICENSE file for licensing details.
"""This file defines the schema for the provider side of the milter interface.

It exposes one interfaces.schema_base.DataBagSchema subclass called:
- ProviderSchema

Examples:
    ProviderSchema:
        app: <empty>
        unit:
          port: 8892
"""
from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field


class MilterProviderData(BaseModel):
    port: int = Field(
        ge=1,
        le=65536,
        description="Milter port.",
        title="Port",
        examples=[8892, 8893],
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for Milter."""

    unit: MilterProviderData


class RequirerSchema(DataBagSchema):
    """Requirer schema for Milter."""
