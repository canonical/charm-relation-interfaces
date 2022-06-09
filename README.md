# Juju Relation Interfaces

This project contains a set of commonly used Juju interfaces and details the expected behaviour
from their requirer and provider charms. Each directory contains an interface definition 
that is made of:
- A README.md file explaining the interface and the provider and requirer behaviour.
- JSON schemas for both the provider and the requirer data bucket content.
- A charms.yaml file that contains the list of charms using the relation.

## Interfaces

| Interface | Status |
| :----- | :-------- |
| [`ingress`](ingress/README.md) | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange?style=flat-square)|
| [`ingress-per-unit`](ingress_per_unit/README.md) | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange?style=flat-square) |
| [`prometheus_remote_write`](prometheus_remote_write/README.md) | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange?style=flat-square) |
| [`tls_certificates`](prometheus_remote_write/README.md) | ![Status: Draft](https://img.shields.io/badge/Status-Draft-orange?style=flat-square) |
