"""This file defines the schemas for the provider and requirer sides of the kratos_external_idp interface.

It exposes two interfaces.schema_base.DataBagSchema subclasses called:
- ProviderSchema
- RequirerSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {
          "providers":[
            "client_id": "client_id"
            "client_secret": "cl1ent-s3cRet"
            "secret_backend": "relation"
            "tenant_id": "4242424242424242"
            "provider": "microsoft"
          ]
        }

    RequirerSchema:
        unit: <empty>
        app: {
          "providers": [
            "redirect_uri": "https://example.kratos.com/self-service/methods/oidc/callback/microsoft"
            "provider_id": "microsoft"
          ]
        }
"""

from enum import Enum
import textwrap
from typing import List, Optional
from pydantic import AnyHttpUrl, BaseModel, Field, field_validator

from interface_tester.schema_base import DataBagSchema


class Url(BaseModel):
    url: AnyHttpUrl


class Provider(Enum):
    microsoft = "microsoft"
    apple = "apple"
    generic = "generic"
    auth0 = "auth0"
    google = "google"
    facebook = "facebook"
    github = "github"
    gitlab = "gitlab"
    slack = "slack"
    spotify = "spotify"
    discord = "discord"
    twitch = "twitch"
    netid = "netid"
    yandex = "yandex"
    vk = "vk"
    dingtalk = "dingtalk"


class SecretBackend(Enum):
    relation = "relation"
    secret = "secret"
    vault = "vault"


class ExternalIdpProvider(BaseModel):
    client_id: str
    client_secret: str
    secret_backend: SecretBackend = "relation"
    provider: Provider
    scope: Optional[str]
    provider_id: Optional[str]
    jsonnet_mapper: Optional[str] = Field(
        description=(
            "A jsonnet file that will be used to map the external claims to Kratos' claims. "
            "For more info see https://www.ory.sh/docs/kratos/reference/jsonnet."
        ),
        examples=[textwrap.dedent(
        """
        local claims = {
            email_verified: false,
        } + std.extVar('claims');

        {
            identity: {
            traits: {
                [if 'email' in claims && claims.email_verified then 'email' else null]: claims.email,
                [if 'name' in claims then 'name' else null]: claims.name,
                [if 'given_name' in claims then 'given_name' else null]: claims.given_name,
                [if 'family_name' in claims then 'family_name' else null]: claims.family_name,
            },
            },
        }
        """)]
    )
    tenant_id: Optional[str]
    private_key: Optional[str]
    private_key_id: Optional[str]
    team_id: Optional[str]
    issuer_url: Optional[str]

    @field_validator("tenant_id")
    def provider_must_be_microsoft(cls, v, info):
        if v and info.data.get("provider") != "microsoft":
            raise ValueError("Provider must be microsoft to use key: `tenant_id`")
        elif not v and info.data.get("provider") == "microsoft":
            raise ValueError("`tenant_id` is required with provider microsoft")
        return v

    @field_validator("private_key", "private_key_id", "team_id")
    def provider_must_be_apple(cls, v, info):
        if v and info.data.get("provider") != "apple":
            raise ValueError(f"Provider must be apple to use key: `{info.data.get('name')}`")
        elif not v and info.data.get("provider") == "apple":
            raise ValueError(f"`{info.data.get('name')}` is required with apple provider")
        return v

    @field_validator("issuer_url")
    def issuer_url_allowed(cls, v, info):
        if v and info.data.get("provider") in ["generic", "auth0"]:
            raise ValueError(f"`issuer_url` not allowed with provider: {info.data.get('provider')}")
        elif not v and info.data.get("provider") in ["generic", "auth0"]:
            raise ValueError("`issuer_url` is required with {values['provider'] provider")
        return v


class KratosExternalIdpProviderData(BaseModel):
    providers: List[ExternalIdpProvider]


class ProviderSchema(DataBagSchema):
    """Provider schema for KratosExternalIdp.
    This relation interface can be used to provide a set of client configurations to Kratos to connect with external providers.
    """
    app: KratosExternalIdpProviderData

    class Config:
        schema_extra = {
            "example": {
                "unit": None,
                "app": {
                    "providers": [
                        {
                            "client_id": "client_id",
                            "client_secret": "cl1ent-s3cRet",
                            "secret_backend": "relation",
                            "tenant_id": "4242424242424242",
                            "provider": "microsoft",
                        }
                    ]
                }
            }
        }

class ExternalIdpRequirer(BaseModel):
    redirect_uri: Url
    provider_id: str


class KratosExternalIdpRequirerData(BaseModel):
    providers: List[ExternalIdpRequirer]


class RequirerSchema(DataBagSchema):
    """Requirer schema for KratosExternalIdp.
    This relation interface can be used from Kratos to provide the redirect_uri of a client that will be used with an external provider.
    """
    app: KratosExternalIdpRequirerData

    class Config:
        schema_extra = {
            "example": {
                "unit": None,
                "app": {
                    "providers": [
                        {
                            "redirect_uri": "https://example.kratos.com/self-service/methods/oidc/callback/microsoft",
                            "provider_id": "microsoft",
                        }
                    ]
                }
            }
        }
