# `grafana-auth`

## Usage

This relation interface describes the expected behavior of any charm aiming to authenticate with `Grafana` with an authentication mode other than the default.

The interface will consist of a `provider` and a `requirer`, the `provider` is expected to allow authentication to `Grafana` (e.g.: `Grafana charm`), the `requirer` will be able to consume the relation and specify an authentication mode and use it to authenticate to `Grafana`.

## Behavior

Both the Requirer and the provider need to adhere to a certain set of criterias to be considered compatible with the interface.

### Provider

- Is expected to allow configuration of authentication mode to `Grafana` as specified by the `requirer`. The modes that can be used are listed in the[\[official documentation \]](https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/)

### Requirer

- Is expected to provide the prefered authentication mode with the required configuration towards the provider using a top-level key in the application databag to group the whole authentication config together.
- Possible modes: 
  - azuread
  - generic_oauth
  - google
  - jwt
  - gitlab
  - ldap
  - okta
  - proxy
  - github
  - anonymous
  - basic

## Relation Data

### Provider
[\[JSON Schema\]](./schemas/provider.json)

### Requirer
[\[JSON Schema\]](./schemas/requirer.json)
The requirer provides the authentication mode and its configuration.

