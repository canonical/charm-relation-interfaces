# `database`

## Usage

This relation interface describes the expected behaviour of any charm claiming to be able to interact with a database.

In most cases, this will be accomplished using the database provider library, although charm developers are free to provide alternative libraries as long as they fulfil the behavioural and schematic requirements described in this document.

## Direction

```mermaid
flowchart TD
    Consumer -- database, extra-user-roles --> Provider
    Provider -- username, password, endpoints --> Consumer
```

As with all Juju relations, the `database` interface consists of two parties: a Provider (database charm), and a Consumer (application charm). The Consumer will be expected to provide a database name, and the Provider will provide new unique credentials (along with other optional fields), which can be used to access the actual database cluster.

## Behavior

Both the Consumer and the Provider need to adhere to criteria to be considered compatible with the interface.

### Consumer

- The consumer leader unit should provide a database name (in the `database` field).
- If several Consumer units provide the `database` field, the value must be identical.
- Different instances of the same Charm (juju applications) will have different relations. Each relation will have unique credentials.
- Different relations names with the same interface name should be used if Consumer need access to multiple databases.
- Different juju applications can have access to the same database name.
- Consumer can provide `extra-user-roles` field if special privileges needed (e.g. `extra-user-roles=admin`).


### Provider
- Provider should create application user inside database cluster and provide `username` and `password` fields.
- Provider should provide the `endpoints` field with a comma-separated list of hosts, which can be used for database connection.
- Provider should provide fields `tls` and `tls-ca` if TLS is configured.
- Provider can provide database-specific fields `read-only-endpoints`, `replset`, `uris`.
- Provider can provide database version field `version`.

## Relation Data

### Consumer

[\[JSON Schema\]](./schemas/provider.json)

Consumer provides database name in `database` unit. Should be placed in the **unit** databag
in at least one unit of the Consumer.

#### Example

```yaml
  relation-info:
  - endpoint: database
    related-endpoint: database
    application-data: {}
    related-units:
      worker-a/0:
        in-scope: true
        data:
          database: myappA
```

### Provider

[\[JSON Schema\]](./schemas/consumer.json)

Provider provides credentials, endpoints, TLS info and database-specific fields. It should be placed in the **application** databag.


#### Example
```yaml
  relation-info:
  - endpoint: database
    related-endpoint: database
    application-data:
      database: myappB
      endpoints: mongodb-k8s-1.mongodb-k8s-endpoints,mongodb-k8s-0.mongodb-k8s-endpoints
      password: Dy0k2UTfyNt2B13cfe412K7YGs07S4U7
      replset: mongodb-k8s
      uris: mongodb://relation-68:Dy0k2UTfyNt2B13cfe412K7YGs07S4U7@mongodb-k8s-1.mongodb-k8s-endpoints,mongodb-k8s-0.mongodb-k8s-endpoints/myappB?replicaSet=mongodb-k8s&authSource=admin
      username: relation-68
```
