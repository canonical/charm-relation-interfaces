# `connect_client`

## Usage

This relation interface describes the expected behavior of any charm claiming to be able to interface with a Kafka Connect cluster as a client/integrator or a provider. For the sake of this document,  `client`, `integrator` and `requirer` all refer to the same concept.

A Kafka Connect integrator will either require a specific `connector` library (which is a bundle of JAR files adhering to Kafka Connect connector interface definit) or not:

- In case it requires a connector library, it should provide the URL of this resource via `plugin-url` parameter on the requirer side. All the required files should be packaged into a single Tarball and served at the provided endpoint. The only requirement here is that the `plugin-url` should be accessible by the Kafka Connect provider.
- In case a connector library is not required (e.g. the case of MirrorMaker integrator), the requirer should fill the `plugin-url` with the sentinel value: `NOT-REQUIRED`.

## Direction

```mermaid
flowchart LR
    Requirer -- plugin-url --> Provider
    Provider -- username, password, endpoints --> Requirer
```

## Behavior

Both the Requirer and the Provider need to adhere to the following criteria, to be considered compatible with the interface.

### Provider

- The provider should download the connector plugins from the `plugin-url` path provided by the requirer and make it available across all Kafka Connect workers. In case it encounters the sentinel value `NOT-REQUIRED`, it should skip this step.
- Is expected to create an application `username` and `password` inside the Kafka Connect cluster after making sure the connector plugins are available on all workers. These credentials could be used on the Kafka Connect REST interface by the requirer.
- Is expected to provide the `endpoints` field with a comma-seperated list of Kafka Connect REST endpoints. Each value in this list also includes the protocol which could be `http` or `https`.
- Is expected to delete an application `username` and `password` from the Kafka Connect cluster when the relation is removed.
- Is expected to cleanup all client plugin files when the relation is removed.

### Requirer

- Is expected to provide the `plugin-url` field specifying the URL at which the connector plugin files are served as a single Tarball, or the sentinel value `NOT-REQUIRED` in case it does not need a plugin.
- Is expected to manage its own connector/task(s) lifecycle by the means of Kafka Connect REST endpoints, using the data provided by the provider.

## Relation Data

### Provider

[\[JSON Schema\]](./schemas/provider.json)

Provider provides credentials and REST endpoint uris. It should be placed in the **application** databag.

#### Example

```yaml
relation-info:
  - endpoint: connect_client
    related-endpoint: connect_client
    application-data:
      username: relation-10
      password: 6Kt3niByjltswXvaO43N9P9vbyUvoBcS
      endpoints: http://10.1.1.100:8083,http://10.1.1.101:8083,http://10.1.1.102:8083
```

### Requirer

[\[JSON Schema\]](./schemas/requirer.json)

Requirer provides (and possibly serves) the `plugin-url`. It should be placed in the **application** databag.

#### Example

```yaml
relation-info:
  - endpoint: connect_client
    related-endpoint: connect_client
    application-data:
        plugin-url: http://10.1.1.200:8080/route/to/plugin
```

