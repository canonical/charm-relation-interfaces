# `vault-transit`

## Usage

This relation interface describes the expected behavior of a charm that integrates with the Vault Transit backend over the `vault-transit` relation.

## Data Flow

```mermaid
flowchart LR
    Provider -- address, token_secret_id --> Requirer
    Requirer
```

## Behavior

Both the Requirer and the Provider need to adhere to criteria to be considered compatible with the interface. Specifically, the Requirer has some operations to perform, and data to provide to the Requirer. The Requirer on the other hand, must configure Vault to autounseal based on the data provided by the Provider.

### Provider

The Provider is expected to

- create a `transit` backend with the path `charm-transit` if it does not already exist
- create an encryption key for the requirer called `charm-transit/keys/${relation_id}` in the `charm-transit` backend
- create a policy for the requirer that provides `update` capabilities on the encryption key
- create a token for this policy, and store it in a Juju secret
  - The secret should contain at least one value: `token`
- provide the Juju secret ID to the Requirer
- provide the URL of the Vault (used in the Vault config for the `address` value)

### Requirer

The Requirer is expected to

- retrieve the token from the Juju secret provided by the Requirer
- configure Vault using a `seal "transit"` stanza and
  - set the `address` to the address provided in the databag
  - set the `key_name` to `charm-transit/keys/${relation_id}`
  - set the `mount_path` to `charm-transit`

## Relation Data

[\[Pydantic Schema\]](./schema.py)

#### Example

TODO

## Limitations

In this iteration, many data points (mount path, key name) are implied, and not configurable. This is likely to change in future versions.

Additionally, this version of the interface focuses purely on using the transit backend for autounseal, although there are other legitimate uses of using the transit backend, which should be considered in the future.
