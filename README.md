# Charm Relation Interfaces

A catalogue of opinionated and standardized interface specifications for charmed operator relations. The purpose of the repository is to outline the behavior and requirements for key interface names, ensuring that charms claiming to implement a certain interface actually are capable of being integrated with each other. 

## Interfaces

| Interface                                                                    | Status                                                              |
| :--------------------------------------------------------------------------- | :-----------------------------------------------------------------: |
| [`database`](interfaces/database/v0/README.md)                               | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
| [`grafana-auth`](interfaces/grafana_auth/v0/README.md)                       | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
| [`ingress`](interfaces/ingress/v0/README.md)                                 | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
| [`ingress_per_unit`](interfaces/ingress_per_unit/v0/README.md)               | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
| [`kafka_client`](interfaces/kafka_client/v0/README.md)                       | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
| [`k8s-service`](interfaces/k8s-service/v0/README.md)                         | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
| [`mongodb_client`](interfaces/mongodb_client/v0/README.md)                   | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
| [`mysql_client`](interfaces/mysql_client/v0/README.md)                       | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
| [`postgresql_client`](interfaces/postgresql_client/v0/README.md)             | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
| [`prometheus_remote_write`](interfaces/prometheus_remote_write/v0/README.md) | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
| [`prometheus_scrape`](interfaces/prometheus_scrape/v0/README.md)             | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |
| [`tls_certificates/v0`](interfaces/tls_certificates/v0/README.md)            | ![Status: Live](https://img.shields.io/badge/Status-Live-darkgreen) |
| [`tls_certificates/v1`](interfaces/tls_certificates/v1/README.md)            | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange)  |


For a more detailed explanation of statuses and how they should be used, see [the legend](LEGEND.md).
