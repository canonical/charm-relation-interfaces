# `grafana-auth`

## Usage

This relation interface describes the expected behavior of any charm caliming to be able to provide or consume `Grafana` authentication configuration data.

The interface will consist of a `provider` and a `requirer`, the `provider` is expected to allow configurable authentication to `Grafana` (e.g.: `Grafana charm`), while the `requirer` should be able to consume the relation and configure the authentication mode to authenticate to `Grafana`.

## Behavior

Both the Requirer and the provider need to adhere to a certain set of criterias to be considered compatible with the interface.

### Provider

- Is expected to allow configuration of authentication mode to `Grafana` as specified by the `requirer`. The modes that can be used are listed in Grafana's [\[official documentation \]](https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/)

### Requirer

- Is expected to provide the prefered authentication mode with the required configuration towards the provider using a top-level key in the application databag to group the whole authentication config together.

## Relation Data

### Provider
[\[JSON Schema\]](./schemas/provider.json)

### Requirer
[\[JSON Schema\]](./schemas/requirer.json)
The requirer provides the authentication mode and its configuration.
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
