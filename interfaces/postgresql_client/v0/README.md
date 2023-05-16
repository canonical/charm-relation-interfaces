# `postgresql_client`

## Usage

This relation interface describes the expected behaviour of any charm claiming to be able to interact with a PostgreSQL database.
Our intent to have different interface names with `<database>_client` pattern (like `mongodb_client`) and the same validation rules for multiple databases (e.g. MySQL, PostgreSQL, MongoDB, etc).

In most cases, this will be accomplished using the database provider library, although charm developers are free to provide alternative libraries as long as they fulfil the behavioural and schematic requirements described in this document.

## Direction

```mermaid
flowchart TD
    Requirer -- database, extra-user-roles --> Provider
    Provider -- database, username, password, endpoints --> Requirer
```

As with all Juju relations, the `database` interface consists of two parties: a Provider (database charm), and a Requirer (application charm). The Requirer will be expected to provide a database name, and the Provider will provide new unique credentials (along with other optional fields), which can be used to access the actual database cluster.

## Behavior

Both the Requirer and the Provider need to adhere to criteria to be considered compatible with the interface.

### Provider
- Is expected to create an application user inside the database cluster when the requirer provides the `database` field.
- Is expected to provide `username` and `password` fields when Requirer provides the `database` field.
- Is expected to provide the `endpoints` field with has address of Primary, which can be used for Read/Write queries.
- Is expected to provide the `database` field with the database that was actually created.
- Is expected to provide optional `enabled-plugins` field with a comma-separated list of plugins that are currently enabled in the database.
- Is expected to provide optional `read-only-endpoints` field with a comma-separated list of hosts or one Kubernetes Service, which can be used for Read-only queries.
- Is expected to provide the `version` field whenever database charm wants to communicate its database version.

### Requirer

- Is expected to provide a database name in the `database` field.
- Is expected to provide identical values in the `database` field if several requirer units provide it in the relation.
- Is expected to have unique credentials for each relation. Therefore, different instances of the same Charm (juju applications) will have different relations with different credentials.
- Is expected to have different relations names on Requirer with the same interface name if Requirer needs access to multiple database charms.
- Is expected to allow multiple different Juju applications to access the same database name.
- Is expected to add any `extra-user-roles` provided by the Requirer to the created user (e.g. `extra-user-roles=admin`).
- Is expected to tolerate that the Provider may ignore the `database` field in some cases and instead use the database name received.

## Relation Data

### Provider

[\[JSON Schema\]](./schemas/provider.json)

Provider provides credentials, endpoints, TLS info and database-specific fields. It should be placed in the **application** databag.


#### Example
```yaml
  relation-info:
  - endpoint: database
    related-endpoint: database
    application-data:
      database: myappB
      enabled-plugins: citext,hstore,pgtrgm,unaccent 
      endpoints: postgresql-k8s-primary:5432
      read-only-endpoints: postgresql-k8s-replicas:5432
      password: Dy0k2UTfyNt2B13cfe412K7YGs07S4U7
      username: relation-68
```

### Requirer

[\[JSON Schema\]](./schemas/requirer.json)

Requirer provides database name. It should be placed in the **application** databag.

#### Example

```yaml
  relation-info:
  - endpoint: database
    related-endpoint: database
    application-data:
      database: myappA
```
