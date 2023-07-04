# `oauth`

## Overview

This relation interface describes the expected behavior of any charm claiming to be able to interface with an OAuth2/OIDC Provider.

## Usage

Charms claiming to provide this interface must implement the OAuth2/OIDC protocol and register a client for each relation. In most cases, this will be accomplished using the [oauth](https://charmhub.io/hydra/libraries/oauth) library, although charm developers are free to provide alternative libraries as long as they fulfill the behavioral and schematic requirements described in this document.

## Direction

The `oauth` interface implements a provider/requirer pattern.
The requirer is a charm that wishes to act as a oauth2 client, and the provider is a charm exposing an OAuth2/OIDC provider.

```mermaid
flowchart TD
    Requirer -- redirect_uri, audience, scope, grant_types, token_endpoint_auth_method --> Provider
    Provider -- issuer_url, authentication_endpoint, token_endpoint, userinfo_endpoint, introspection_endpoint, jwks_endpoint, client_id, client_secret_id, scope, groups --> Requirer
```

## Behavior

The requirer and the provider must adhere to a certain set of criteria to be considered compatible with the interface.

### Provider

- Is expected to provide its endpoints(authentication_endpoint, token_endpoint, userinfo_endpoint, introspection_endpoint and jwks_endpoint) in the relation databag.
- Is expected to provide the issuer_url in the relation databag.
- Is expected to provide the supported scopes in the databag.
- Is expected to register a client and provide the client_id in the databag.
- Is expected to register a client, place the client_secret in a juju secret and provide the juju secret ID in the databag (client_secret_id).
- Is expected to provide the groups claim, if one is available.

As mentioned above the field client_secret_id holds the id of a Juju Secret, this means that the charms implementing the relation must be running on Juju >3 in order be able to use Juju secrets.

### Requirer

- Is expected to provide a user accessible redirect_uri using the HTTPS scheme.
- Is expected to provide an audience for the issued tokens, if extra audience are required.
- Is expected to provide the grant_types and token_endpoint_auth_method it wishes to use.
- Is expected to provide the scopes that should be allowed for this client.

## Relation Data

### Provider

[\[JSON Schema\]](./schemas/provider.json)

Provider provides its endpoints, configurations and the client credentials. It should be placed in the **application** databag.

#### Example

```yaml
related-units: {}
application_data: {
  "issuer_url": "https://auth_server_public_url/",
  "authorization_endpoint": "https://auth_server_public_url/authorize",
  "token_endpoint": "https://auth_server_public_url/token",
  "introspection_endpoint": "https://auth_server_public_url/introspect",
  "userinfo_endpoint": "https://auth_server_public_url/userinfo",
  "jwks_endpoint": "https://auth_server_public_url/jwks",
  "scope": "openid profile email phone",
  "client_id": "some_id",
  "client_secret_id": "42174217421742",
}
```

### Requirer

[\[JSON Schema\]](./schemas/requirer.json)

Requirer requires its client configurations. It should be placed in the **application** databag.

#### Example
```yaml
related-units: {}
application-data: {
  "redirect_uri": "https://some_url/callback",
  "audience": [],
  "scope": "openid email",
  "grant_types": ["authorization_code"],
  "token_endpoint_auth_method": "client_secret_basic"
}
```
