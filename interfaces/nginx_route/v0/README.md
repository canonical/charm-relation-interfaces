# `nginx-route`

## Overview

This relation interface describes the expected behaviour of any charm 
interfacing with Kubernetes Nginx ingress resources.

## Usage

An application charm can use the `nginx-route` relation to request the creation
of a Nginx ingress resource in the Kubernetes cluster. The specific 
configuration of the ingress resources can be controlled by the data provided
by the relation's requirer. The [`nginx_route` charm library](https://charmhub.io/nginx-ingress-integrator/libraries/nginx_route)
can be used to handle the provider and requirer sides of this relation.

## Direction

The `nginx-route` interface is a one-way relation. The requirer of this relation
provides the configuration for the required ingress resources as relation data,
and the provider does not return anything in the relation.

## Behavior

The requirer and the provider must adhere to a certain set of criteria to be 
considered compatible with the interface.

### Provider

- Is expected to create ingress resources in the Kubernetes cluster if the 
requirer's requirements are valid.
- Is expected to display an error message in the charm status and ignore 
requirer's request, if the request specified by the requirer is not valid.
- Is expected to create ingress resources with host-based routing.

### Requirer

- Is expected to provide a valid ingress resource configuration.

## Relation Data

### Provider

The provider does not provide anything in the relation databag.

[\[Pydantic Schema\]](./schema.py)

### Requirer

The `nginx-route` relation uses the same set of data as in the charm 
configuration of the Nginx ingress integrator charm, with the exception that
`service-hostname`, `service-name`, `service-port`, and `service-namespace`
are required in the relation data.

[\[Pydantic Schema\]](./schema.py)

#### Example
```yaml
application-data:
  service-hostname: example.test
  service-name: test-app
  service-port: 8080
  service-namespace: test-namespace
```
