# `kafka-client`

## Usage

This relation interface describes the expected behavior of any charm claiming to be able to interface with a Kafka cluster as a client. For the majority of charms seeking to relate to a Kafka cluster, they will seek to do so either as a producer, consumer or admin client.

- Producers can expect their desired topic/wildcard to be granted `WRITE`, `DESCRIBE`, `CREATE` topic ACLs matching their application credentials upon relation. Producer clients then can create their own topics using whichever client-library they wish, setting any topic level configuration then (e.g `replication-factor` and `partitions`).
- Consumers can expect to be granted ACLs for a specified topic with `READ`, `DESCRIBE` on topic, and `READ` on consumer-group upon relation.
- Admins can expect to be granted super-user permissions for their application credentials upon relation.

## Direction

```mermaid
flowchart TD
    Requirer -- role, topic, group --> Provider
    Provider -- username, password, uris, endpoints, zookeeper_uris --> Requirer
```

## Behavior

Both the Requirer and the Provider need to adhere to the criteria, to be considered compatible with the interface.

### Provider
- Is expected to create an application `username` and `password` inside the kafka cluster when the requirer relates to the kafka cluster.
- Is expected to provide the `uris` field with a comma-seperated list of broker uris, which can be used for cluster connection.
- Is expected to provide the `endpoints` field with a comma-seperated list of broker IP addresses.
- Can optionally provide the `zookeeper_uris` field with a comma-seperated list of ZooKeeper server uris and Kafka cluster zNode, if the requirer `role` is set to `admin`

### Requirer
- Can optionally provide the `role` field specifying the expected role of the client application (e.g `role=producer`, `role=consumer`, `role=admin`).
- Can optionally provide the `topic` field specifying the topic that the requirer charm needs permissions to create (for `role=producer`), or consume (for `role=consumer`). If `role` is set, this field is expected.
- Can optionally provide the desired consumer group for a requirer unit in the `group` field. If `role=consumer`, this field is expected.

## Relation Data

### Provider

[\[JSON Schema\]](./schemas/provider.json)

Provider provides application credentials and server connection uris. It should be placed in the **application** databag.


#### Example
```yaml
  relation-info:
  - endpoint: kafka_client
    related-endpoint: kafka_client
    application-data:
      username: user123
      password: Dy0k2UTfyNt2B13cfe412K7YGs07S4U7
      uris: 10.141.78.155:9092,10.141.78.62:9092,10.141.78.186:9092
      endpoints: 10.141.78.155,10.141.78.62,10.141.78.186
      zookeeper_uris: 10.141.78.133:2181,10.141.78.50:2181,10.141.78.45:2181/kafka

```

### Requirer

[\[JSON Schema\]](./schemas/requirer.json)

Requirer provides client connection uri, and optionally provides user-specified credentials, appliation role and topic. It should be placed in the **application** databag.
Requirer provides consumer group name if the requirer sets it's role as consumer. It should be placed in the **unit** databag.

#### Example

```yaml
  relation-info:
  - endpoint: kafka_client
    related-endpoint: kafka_client
    application-data:
        role: consumer
        topic: special-topic
    related-units:
        worker/0:
            in-scope: true
            data:
                group: group-A
        worker/1:
            in-scope: true
            data:
                group: group-B

```
