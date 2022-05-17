# `database`

## Usage

This relation interface describes the expected behaviour of any charm claiming to be able to interact with a database.
Our intent to have different interface names with `<database>-client` pattern (like `mongodb-client`) and the same validation rules for multiple databases (e.g. MySQL, PostgreSQL, MongoDB, etc).

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

- Is expected that the Consumer leader unit provides a database name (in the `database` field).
- Is expected to have the identical value of the `database` field if several Consumer units provide it in the relation.
- Is expected to have unique credentials for each relation. Therefore, different instances of the same Charm (juju applications) will have different relations with different credentials.
- Is expected to have different relations names on Consumer with the same interface name if Consumer needs access to multiple database charms.
- Is expected to allow multiple different Juju applications to access the same database name.
- Is expected to add any `extra-user-roles` provided by the Consumer to the created user (e.g. `extra-user-roles=admin`).


### Provider
- Is expected that the Provider creates an application user inside the database cluster and provides `username` and `password` fields when Consumer provides the `database` field.
- Is expected to provide the `endpoints` field with a comma-separated list of hosts, which can be used for database connection.
- Is expected to provide fields `tls` and `tls-ca` if TLS is configured.
- Is expected to provide optional database-specific fields,  like `read-only-endpoints`, `replset`, `uris`.
- Is expected to provide the `version` field whenever database charm wants to communicate its database version.

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
