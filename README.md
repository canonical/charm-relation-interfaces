# Charm Relation Interfaces

A catalogue of opinionated and standardized interface specifications for charmed operator relations. The purpose of the repository is to outline the behavior and requirements for key interface names, ensuring that charms claiming to implement a certain interface actually are capable of being integrated with each other.

## Contributing
To contribute an interface specification, open a pull request containing a `README.md`, json schemas for both sides of the relation, as well as a `charms.yaml` file consisting of a list of any `providers` and `consumers` known to adhere to the specification. See the [grafana-auth](https://github.com/canonical/charm-relation-interfaces/tree/main/interfaces/grafana_auth/v0) interface for examples of what to include and how it should be structured. For interface schemas, make sure to include **both the unit and application databag** in your schema, and also make sure to set `additionalProperties` to `true` as we want to be able to keep it extendable.

To quickly get started, you can copy the `interfaces/__template__` folder to create a basic template.

## Interfaces

| Category      | Interface                                                                    |                               Status                                |
|---------------|:-----------------------------------------------------------------------------|:-------------------------------------------------------------------:|
| Data          | [`mysql_client`](interfaces/mysql_client/v0/README.md)                       | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
|               | [`postgresql_client`](interfaces/postgresql_client/v0/README.md)             | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
|               | [`mongodb_client`](interfaces/mongodb_client/v0/README.md)                   | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
|               | [`kafka_client`](interfaces/kafka_client/v0/README.md)                       | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
|               | [`opensearch_client`](interfaces/opensearch_client/v0/README.md)             | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
|               | [`database_backup`](interfaces/database_backup/v0/README.md)                 | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
| Identity      | [`hydra_endpoints`](interfaces/hydra_endpoints/v0/README.md)                 | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
|               | [`oauth`](interfaces/oauth/v0/README.md)                                     | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
| Observability | [`grafana_auth`](interfaces/grafana_auth/v0/README.md)                       | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
|               | [`ingress`](interfaces/ingress/v0/README.md)                                 | ![Status: Live](https://img.shields.io/badge/Status-Live-darkgreen) |
|               | [`ingress_per_unit`](interfaces/ingress_per_unit/v0/README.md)               | ![Status: Live](https://img.shields.io/badge/Status-Live-darkgreen) |
|               | [`prometheus_remote_write`](interfaces/prometheus_remote_write/v0/README.md) | ![Status: Live](https://img.shields.io/badge/Status-Live-darkgreen) |
|               | [`prometheus_scrape`](interfaces/prometheus_scrape/v0/README.md)             | ![Status: Live](https://img.shields.io/badge/Status-Live-darkgreen) |
| Metadata      | [`k8s-service`](interfaces/k8s-service/v0/README.md)                         | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
| Security      | [`tls_certificates/v0`](interfaces/tls_certificates/v0/README.md)            | ![Status: Live](https://img.shields.io/badge/Status-Live-darkgreen) |
|               | [`tls_certificates/v1`](interfaces/tls_certificates/v1/README.md)            | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
| Storage       | [`s3`](interfaces/s3/v0/README.md)                                           | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |

For a more detailed explanation of statuses and how they should be used, see [the legend](https://github.com/canonical/charm-relation-interfaces/blob/main/LEGEND.md).

