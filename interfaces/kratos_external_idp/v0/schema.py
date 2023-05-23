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
from typing import List, Optional
from pydantic import AnyHttpUrl, BaseModel, validator

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
    jsonnet: Optional[str]
    tenant_id: Optional[str]
    private_key: Optional[str]
    private_key_id: Optional[str]
    team_id: Optional[str]
    issuer_url: Optional[str]

    @validator("tenant_id")
    def provider_must_be_microsoft(cls, v, values):
        if v and values["provider"].value != "microsoft":
            raise ValueError("Provider must be microsoft to use key: `tenant_id`")
        elif not v and values["provider"].value == "microsoft":
            raise ValueError("`tenant_id` is required with provider microsoft")
        return v

    @validator("private_key", "private_key_id", "team_id", always=True)
    def provider_must_be_apple(cls, v, values, field):
        if v and values["provider"].value != "apple":
            raise ValueError(f"Provider must be apple to use key: `{field.name}`")
        elif not v and values["provider"].value == "apple":
            raise ValueError(f"`{field.name}` is required with apple provider")
        return v

    @validator("issuer_url")
    def issuer_url_allowed(cls, v, values):
        if v and values["provider"].value in ["generic", "auth0"]:
            raise ValueError(f"`issuer_url` not allowed with provider: {values['provider']}")
        elif not v and values["provider"].value in ["generic", "auth0"]:
            raise ValueError("`issuer_url` is required with {values['provider'] provider")
        return v


class KratosExternalIdpProviderData(BaseModel):
    providers: List[ExternalIdpProvider]

class ProviderSchema(DataBagSchema):
    """Provider schema for KratosExternalIdp."""
    app: KratosExternalIdpProviderData


class ExternalIdpRequirer(BaseModel):
    redirect_uri: Url
    provider_id: str


class KratosExternalIdpRequirerData(BaseModel):
    providers: List[ExternalIdpRequirer]


class RequirerSchema(DataBagSchema):
    """Requirer schema for KratosExternalIdp."""
    app: KratosExternalIdpRequirerData

