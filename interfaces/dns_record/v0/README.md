# `dns_record`

## Usage

This relation interface describes the expected behavior of any charm claiming to be able to interface with a DNS record Provider.

## Direction

The `dns_record` interface implements a provider/requirer pattern. The requirer is a charm that wishes to create a set of DNS records, and the provider is the charm managing those.
```mermaid
flowchart TD
  Requirer -- dns_domains, dns_entries --> Provider
  Provider -- dns_domains, dns_entries --> Requirer
```

## Behavior

The following is the criteria that a Provider and Requirer need to adhere to be compatible with this interface.

### Provider

- Is expected to provide a list of dns_domains and a list of dns_entries in the relation databag, each containing the domain, the status and optionally the description corresponding to the dns_domains and dns_entries requirested by the requirer.
- Is expected to authenticate requests for dns_domains based on internal business rules/processes at the organisation where this charm is deployed.

### Requirer

- Is expected to provide a list of dns_domains in the relation databag, each containing the domain it is requesting a DNS record for, the username and the password containing a juju secret for the provider to authenticate the request.
- Is expected to provide a list of dns_entries mains in the relation databag, containing at least the dns-domain, the host-label and record-data. The dns-domain must be present in the list of dns_domains for authentication.
- Is expected to authenticate requests for dns_domains based on internal business rules/processes at the organisation where this charm is deployed. The credentials need to be negotiated outside of the charm relation.

## Relation Data

### Provider

[\[JSON Schema\]](./schemas/provider.json)

Provider provides the result of the requirer request. It should be placed in the application databag.

#### Example
```json
  "application-data": {
    "dns_domains": [
      {
        "uuid": "550e8400-e29b-41d4-a716-446655440000",
        "status": "invalid_credentials",
        "description": "invalid_credentials"
      },
      {
        "uuid": "550e8400-e29b-41d4-a716-446655440001",
        "status": "approved"
      }
    ],
    "dns_entries": [
      {
        "uuid": "550e8400-e29b-41d4-a716-446655440002",
        "status": "invalid_credentials",
        "description": "invalid_credentials"
      },
      {
        "uuid": "550e8400-e29b-41d4-a716-446655440003",
        "status": "approved"
      }
    ]
  }

```

### Requirer

[\[JSON Schema\]](./schemas/requirer.json)

Requirer request the details of one or more DNS records. It should be placed in the application databag.

#### Example

```json
  "application-data": {
    "dns_domains": [
      {
        "uuid": "550e8400-e29b-41d4-a716-446655440000",
        "domain": "cloud.canonical.com",
        "username": "user1",
        "password_id": "secret:123213123123123123123"
      },
      {
        "uuid": "550e8400-e29b-41d4-a716-446655440001",
        "domain": "staging.ubuntu.com",
        "username": "user2",
        "password_id": "secret:123213123123123123122"
      }
    ],
    "dns_entries": [
      {
        "uuid": "550e8400-e29b-41d4-a716-446655440002",
        "domain": "cloud.canonical.com",
        "host_label": "admin",
        "ttl": 600,
        "record_class": "IN",
        "record_type": "A",
        "record_data": "91.189.91.48"
      },
      {
        "uuid": "550e8400-e29b-41d4-a716-446655440003",
        "domain": "staging.canonical.com",
        "host_label": "www",
        "record_data": "91.189.91.47"
      }
    ]
  }
```
