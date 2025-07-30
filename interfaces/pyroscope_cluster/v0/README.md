# `pyroscope_cluster`

## Usage

`pyroscope_cluster` is an interface meant to exchange cluster configuration in distributed Pyroscope deployments.
Multiple [Pyroscope worker](https://github.com/canonical/pyroscope-k8s-operator/tree/main/worker) applications can relate to a [Pyroscope coordinator](https://github.com/canonical/pyroscope-k8s-operator/tree/main/coordinator) application over the `pyroscope_cluster` interface, and send their role and topology, in order to join the cluster.
The coordinator will use the same relation to convey to the workers back the configuration that they must run with.

## Direction

This interface implements a provider/requirer pattern. The coordinator charm is the provider of the relation, the worker charm is the requirer. Information flows back and forth: first the requirer shares some data necessary for the coordinator to know the role of the worker, then the provider replies back with the configuration it should run with. 

```mermaid
flowchart TD
    Requirer -- Role, JujuTopology --> Provider
    Provider -- Config --> Requirer
```

## Behavior

This is what is expected of the providers and the requirers of this interface:

### Provider
The provider is expected to...
- update the gossip rings in all configurations with the addresses of all worker units that are joining the cluster (regardless of their role).
- share the exact same configuration to all nodes, regardless of the role they declare, via application databag.

### Requirer
The requirer application is expected to...
- publish its role as soon as possible via application databag.  
Each requirer unit is expected to...
- publish its address and JujuTopology as soon as possible, via unit databag.

## Relation Data

Describe the contents of the databags, and provide schemas for them.

[\[Pydantic Schema\]](./schema.py)

#### Example
Here is a yaml example of a valid databag state (for the whole relation).
```yaml
provider:
  app: 
    config: 
      # <a very large chunk of yaml, conforming to Pyroscope configuration specification: https://grafana.com/docs/pyroscope/latest/configuration/#configure-pyroscope>
  unit: {}
  
requirer:
  app: 
    role: querier
  unit: 
   juju_topology: 
     model: "mymodel", 
     model_uuid: "1231234120941234", 
     application: "pyroscope-querier", 
     charm_name: "pyroscope-worker-k8s", 
     unit: "pyroscope-querier/2", 
```
