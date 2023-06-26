# `ingress-per-unit`

## Usage

This relation interface describes the expected behavior of any charm claiming to be able to provide or consume ingress per unit data.

In most cases, this will be accomplished using the [ingress library](https://github.com/canonical/traefik-k8s-operator/blob/main/lib/charms/traefik_k8s/v1/ingress_per_unit.py), although charm developers are free to provide alternative libraries as long as they fulfill the behavioral and schematic requirements described in this document.

## Direction
The `ingress-per-unit` interface implements a provider/requirer pattern.
The requirer is a charm that wishes to receive ingress per unit, and the provider is a charm able to provide it.

```mermaid
flowchart TD
    Requirer -- IngressData --> Provider
    Provider -- IngressPerUnit --> Requirer
```

## Behavior

The requirer and the provider need to adhere to a certain set of criteria to be considered compatible with the interface.

### Provider

- Is expected to provide ingress for remote units requesting it.
- Is expected to respect the ingress parameters sent by the requirer via unit relation data: hostname, port and model name (namespace).
- Is expected to publish the ingress url via relation data, as a mapping from unit names to urls.

### Requirer

- Is expected to be able to provide a hostname, a port, a unit name and a model name (namespace). 

## Relation Data

### Provider

[\[JSON Schema\]](./schemas/provider.json)

Exposes a `urls` field containing a mapping from unit name to the url at which ingress is available for that unit. Should be placed in the **application** databag, encoded as yaml and nested in a "data" field.

#### Example

```yaml
application_data: {
  urls: { 
    unit_name: "http://foo.bar:80/model_name-unit_name/0" 
  }
}
```

### Requirer

[\[JSON Schema\]](./schemas/requirer.json)

Exposes the unit name, model name, hostname and port at which ingress should be provided. Should be placed in the **unit** databag of _each unit_ of the requirer application.

#### Example
```yaml
unit-data: {
 name: "unit-name",
 host: "hostname",
 port: 4242,
 model: "model-name"
}
```


