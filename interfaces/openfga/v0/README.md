# `openfga`

## Usage

This relation interface describes the expected behaviour of any charm claiming to be able to interact with a OpenFGA.

In most cases, this will be accomplished using the [openfga library](https://github.com/canonical/cs-openfga/blob/main/charms/openfga-k8s/lib/charms/openfga_k8s/v0/openfga.py), although charm developers are free to provide alternative libraries as long as they fulfil the behavioural and schematic requirements described in this document.

## Direction

```mermaid
flowchart TD
    Requirer -- openfga, store-name --> Provider
    Provider -- openfga, store-id, token, address, scheme, port --> Requirer
```

As with all Juju relations, the `openfga` interface consists of two parties: a Provider (openfga charm), and a Requirer (application charm). The Requirer will be expected to provide an authentication store name, and the Provider will provide new unique credentials (along with other optional fields), which can be used to access the OpenFGA store.

## Behavior

Both the Requirer and the Provider need to adhere to criteria to be considered compatible with the interface.

### Provider
- Is expected to create an authentication store in OpenFGA when the requirer provides the `store_name` field.
- Is expected to provide `token`, `store_id`, `address`, `scheme` and `port` fields in the *application* databag, which can be used for OpenFGA connection, when Requirer provides the `store_name` field.

### Requirer

- Is expected to provide an authentication store name in the `store_name` field of the *application* databag.

## Relation Data

### Provider

[\[JSON Schema\]](./schemas/provider.json)

Provider provides `token`, `store_id`, `address`, `scheme` and `port` fields. It should be placed in the **application** databag.


#### Example
```yaml
  relation-info:
  - endpoint: openfga
    related-endpoint: openfga
    application-data:
      token: "test-token"
      store_id: "01GK13VYZK62Q1T0X55Q2BHYD6"
      address: "10.10.0.17"
      scheme: "http"
      port: "8080"
```

### Requirer

[\[JSON Schema\]](./schemas/requirer.json)

Requirer provides authorization store name. It should be placed in the **application** databag.

#### Example

```yaml
  relation-info:
  - endpoint: openfga
    related-endpoint: openfga
    application-data:
      store_name: "test-store"
```
