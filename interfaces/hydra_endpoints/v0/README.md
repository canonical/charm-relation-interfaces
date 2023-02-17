# `hydra_endpoints`

## Usage

This relation interface describes the expected behavior of provider ([Ory Hydra](https://github.com/canonical/hydra-operator))
and requirer ([Ory Kratos](https://github.com/canonical/kratos-operator)) sides of relation.

Kratos requires `oauth2_provider` parameter in order to be able to interact with Hydra. This parameter is the Hydra's admin API endpoint,
which will usually be exposed through Ingress using `traefik-k8s` charm.
The interface will provide admin and public endpoints, in case any other charm belonging to the IAM bundle requires them both.

The purpose of this relation is to facilitate integration between the two charms by passing the endpoints from Hydra to Kratos.

For now, the only known requirer is Kratos and Hydra is the only provider, however the interface may be reused by other charms,
as long as they provide or require admin and/or public endpoints.

## Direction

The interface will consist of a provider and a requirer. The provider is expected to supply its public and admin endpoints,
while the requirer will just consume the information.

```mermaid
flowchart
    Requirer -- --> Provider
    Provider -- hydra_admin_endpoint, hydra_public_endpoint --> Requirer
```

## Behavior

The provider must be able to supply admin and public endpoints. There are no criteria for the requirer as it's supposed to just consume the relation data.

### Provider

- Is expected to send the public and admin URLs to the interface.
  The url is expected to have the following structure:

    > `http://[traefik-hostname]:[traefik-port]/[app-name]-[model-name]/`
    

### Requirer

- Is expected to consume the relation data.

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

#### Example
```json
{
"application_data": {
  "admin_endpoint": "admin-endpoint",
  "public_endpoint": "public-endpoint"
}
}
```
