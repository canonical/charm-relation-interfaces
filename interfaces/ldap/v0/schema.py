"""This file defines the schemas for the provider and requirer sides of this
relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from pydantic import AnyUrl, BaseModel, Field

from interface_tester.schema_base import DataBagSchema


class LdapProviderData(BaseModel):
    ldap_url: AnyUrl = Field(
        description="The LDAP URL",
        example="ldap://ldap.canonical.com",
    )
    base_dn: str = Field(
        description="The base entry as the starting point for LDAP search "
                    "operation",
        example="dc=canonical,dc=com",
    )
    bind_dn: str = Field(
        description="The DN of the bind account",
        example="cn=admin,ou=engineering,dc=canonical,dc=com",
    )
    bind_password: str = Field(
        description="The juju secret URI of the bind account's password",
        example="secret://59060ecc-0495-4a80-8006-5f1fc13fd783/cjqub6vubg2s77p3nio0"
    )
    auth_method: str = Field(
        description="The LDAP authentication method",
        example="simple",
    )


class LdapRequirerData(BaseModel):
    app: str = Field(
        description="The Juju application name of the requirer charmed "
                    "operator",
    )
    model: str = Field(
        description="The Juju model name of the requirer charmed operator",
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of the ldap interface."""
    app: LdapProviderData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of the ldap interface."""
    app: LdapRequirerData
