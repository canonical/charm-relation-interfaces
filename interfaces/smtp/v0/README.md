# `smtp`

## Overview

This relation interface specification describes the expected behavior of charms integrating over the `smtp` Juju interface to provide or consume SMTP data.

## Usage

In most cases, this will be accomplished using the [smtp library](https://github.com/canonical/smtp-integrator-operator/blob/main/lib/charms/smtp_integrator/v0/smtp.py), although charm developers are free to provide alternative libraries as long as they fulfil the behavioural and schematic requirements described in this document.

## Direction

The `smtp` interface implements a provider/requirer pattern.
The requirer is a charm that requires SMTP details to connect to an SMTP server, and the provider is a charm holding those details.

```mermaid
flowchart TD
    Provider -- host, port, user, password_id, auth_type, transport_security, domain --> Requirer
```

or alternatively, if secrets are not supported by either sides

```mermaid
flowchart TD
    Provider -- host, port, user, password, auth_type, transport_security, domain --> Requirer
```

## Behavior

The requirer and the provider must adhere to a certain set of criteria to be considered compatible with the interface.

### Provider

- Is expected to provide the SMTP details so that the requirer can connect.

### Requirer

- Is not expected to publish anything

## Relation Data

### Provider

[\[Pydantic Schema\]](./schema.py)

Provider publishes the SMTP configuration. It should be placed in the **application** databag.

#### Example

```yaml
related-units: {}
application_data: {
  "host": "example.com",
  "port": "587",
  "user": "example_user",
  "password_id": "01548499c9233d4612352c989162d940f6a9e6f6d5cc058dfcf66f51575e09c2",
  "auth_type": "plain",
  "transport_security": "tls",
  "domain": "example.com",
}
```
