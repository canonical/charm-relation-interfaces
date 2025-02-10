"""This file defines the schemas for the provider and requirer sides of this
relation interface.

It must expose two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema
"""

from typing import List, Optional

from interface_tester.schema_base import DataBagSchema
from pydantic import AnyUrl, BaseModel, Field


class LdapProviderData(BaseModel):
    urls: List[AnyUrl] = Field(
        description="List of LDAP URLs",
        title="LDAP URLs",
        example=["ldap://ldap.canonical.com:3893", "ldap://ldap.ubuntu.com:3893"],
    )
    base_dn: str = Field(
        description="The base entry as the starting point for LDAP search "
                    "operation",
        title="Base DN",
        example="dc=canonical,dc=com",
    )
    bind_dn: str = Field(
        description="The distinguished name (DN) of the bind account",
        title="Bind DN",
        example="cn=admin,ou=engineering,dc=canonical,dc=com",
    )
    bind_password_secret: str = Field(
        description="The juju secret ID of the bind account's password",
        example="secret://59060ecc-0495-4a80-8006-5f1fc13fd783/cjqub6vubg2s77p3nio0"
    )
    auth_method: str = Field(
        description="The LDAP authentication method",
        title="Authentication Method",
        example="simple",
    )
    starttls: bool = Field(
        description="The indicator of StartTLS operation enabled or not",
        title="StartTLS",
        example=True,
    )


class LdapRequirerData(BaseModel):
    user: Optional[str] = Field(
        description="The user name provided by the requirer charmed operator",
    )
    group: Optional[str] = Field(
        description="The group name provided by the requirer charmed operator",
    )


class ProviderSchema(DataBagSchema):
    """The schema for the provider side of the ldap interface."""
    app: LdapProviderData


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of the ldap interface."""
    app: LdapRequirerData
