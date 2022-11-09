# `kratos_external_idp`

## Usage
This relation interface describes the expected behavior of any charm claiming to be able to interface with an Ory Kratos server as an integrator between an OIDC Provider external to the Juju model  and the Kratos charm. Charms providing this relation interface are expected to facilitate the automatic management of the client credentials from the Kratos server.

It is expected that an administrator will create the client credentials on the OP that will be used to authenticate Kratos, and retrieve a `client_id` and a `client_secret`. The Administrator will then manually add these secrets to any Charm seeking to provide the `kratos_external_idp` relation. When a Kratos Charm relates to a Provider Charm on this interface, these secrets are to be passed to the Kratos Charm across relation data. The Kratos charm then will place in the relation the redirect_uri and the provider_id for this client. Finally the admin has to provide the redirect_uri to the external OP.

## Terminology

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC2119](https://www.rfc-editor.org/rfc/rfc2119).

## Direction

```mermaid
flowchart
    Requirer -- provider_id, redirect_uri --> Provider
    Provider -- client_id, provider, secret_backend, microsoft, apple, generic, auth0, google, facebook, github, gitlab, slack, spotify, discord, twitch, netid, yandex, vkontakte, dingtalk --> Requirer
```

## Behavior

The Provider MUST adhere to the criteria, to be considered compatible with the interface.

### Provider
- MUST provide the `client_id` field with the value necessary for establishing an authorized connection to the external OP
- MUST provide the `provider` field with the type of the external OP. `provider` must be one of: `generic`, `google`, `facebook`, `microsoft`, `github`, `apple`, `gitlab`, `auth0`, `slack`, `spotify`, `discord`, `twitch`, `netid`, `yander`, `vk`, `dingtalk`.
- MUST provide the `secret_backend` field with information about backend used to store the sensitive information (`client_secrets`, `apple_private_keys`). The `secret_backend` field MUST have one of the following values: `relation`, `secret`, `vault`.
- MUST provide the field with the value of the provider field and the necessary information.
- If `provider` is any of `generic` or `auth0` then the Provider MUST provider the `client_secret` and `issuer_url` fields under the corresponding key.
- If `provider` is any of `google`, `facebook`, `github`, `gitlab`, `slack`, `spotify`, `discord`, `twitch`, `netid`, `yandex`, `vkontakte` or `dingtalk` then the Provider MUST provide the `client_secret` field under the corresponding key.
- If `provider` is `microsoft` then the Provider MUST provide the `client_secret` and `tenant_id` fields under the corresponding key.
- If `provider` is `apple` then the Provider MUST provide the `team_id`, `private_key_id` and `private_key` fields under the corresponding key.

### Requirer
- MUST provide the `redirect_uri` field with a valid uri.
- MUST provide the `provider_id` field with the ID, that Kratos provided to this external provider

## Relation Data

### Provider

[\[JSON Schema\]](./schemas/provider.json)

Provider provides client credentials and information about the external OP. It MUST be placed in the **application** databag.

#### Example
```yaml
  relation-info:
  - endpoint: kratos_external_idp
    relation-endpoint: kratos_external_idp
    application_data:
      client_id: client_id
      provider: microsoft
      secret_backend: relation
      microsoft:
        client_secret: cl1ent-s3cRet
        tenant_id: 4242424242424242
```

### Requirer

[\[JSON Schema\]](./schemas/requirer.json)

Requirer provides redirect_uri and provider_id. It should be placed in the **application** databag.

#### Example

```yaml
  relation-info:
  - endpoint: kratos_external_idp
    related-endpoint: kratos_external_idp
    application-data:
        redirect_uri: https://example.kratos.com/self-service/methods/oidc/callback/callback
        provider_id: microsoft
```

