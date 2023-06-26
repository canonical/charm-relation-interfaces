# `hydra_endpoints`

## Overview

This relation interface describes the expected behavior of charms claiming to be able to provide or consume a hydra endpoint.

## Usage

The interface will provide admin and public endpoints, in case any other charm belonging to the IAM bundle requires them both.

## Direction

The interface will consist of a provider and a requirer. The provider is expected to supply its public and admin endpoints,
while the requirer will just read the information from the application databag.

```mermaid
flowchart
    Requirer ----> Provider
    Provider -- hydra_admin_endpoint, hydra_public_endpoint --> Requirer
```

## Behavior

Both the requirer and the provider need to adhere to a certain set of criteria to be considered compatible with the interface:

### Provider

- Is expected to serve admin and public API endpoints 
- Is expected to write the public and admin URLs to the application databag.

### Requirer

- Is expected to consume the relation data to set up integration with Hydra.

## Relation Data

### Provider

[\[JSON Schema\]](./schemas/provider.json)


#### Example


```json
{
  "application_data": {
    "admin_endpoint": "admin-endpoint",
    "public_endpoint": "public-endpoint"
  }
}
```

### Requirer

[\[JSON Schema\]](./schemas/requirer.json)

n/a
