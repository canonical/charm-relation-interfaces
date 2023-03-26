# `cos_agent`

## Usage

This relation interface describes the expected behavior of any charm claiming to be able to provide or require the `cos_agent` interface.

In most cases, this will be accomplished using the [`cos_agent` library](https://charmhub.io/grafana-agent/libraries/cos_agent), although charm developers are free to provide alternative libraries as long as they fulfill the behavioral and schematic requirements described in this document.

## Direction

```mermaid
flowchart TD
    Provider -- "relation_name
    metrics_endpoints
    metrics_rules_dir
    logs_rules_dir
    recursive_rules_dir
    log_slots
    dashboard_dirs
    refresh_events" --> Requirer
    Requirer -- refresh_events --> Provider
```

As all Juju relations, the `cos_agent` interface consists of a provider and a requirer. In this case the `Provider` side of the relationship may provide telemetry settings, if not, the required side will use default values.

## Behavior

Since this interface is meant to be simple and lightweight each telemetry parameter in the `Provider` side is optional, if some of these are not provided, dafault values will be used.

### Provider

- Is expected to be able to provide metrics endpoints to be scraped.
- Is expected to be able to provide a directory containing Prometheus style metrics rules files.
- Is expected to be able to provide a directory containing Loki style rules files.
- Is expected to be able to inform if metrics and logs rules directories should be scanned recursively.
- Is expected to be able to provide snap slots to connect to for scraping logs.
- Is expected to be able to provide a list of directories containing Grafana dashboard files.
- Is expected to be able to provide a list of events on which to refresh relation data.


### Requirer
- Is expected to be able to scrape Prometheus metrics from metrics endpoints and remote-write these metrics to Prometheus and Prometheus compatible systems.
- Is expected to be able to forward alert rules exposed over the relation data bag to Prometheus.
- Is expected to be able to forward logs from the Provider to Loki.
- Is expected to be able to forward alert rules exposed over the relation data bag to Loki.
- Is expected to be able to forward Grafana Dashboards exposed over the relation data bag to Grafana.


## Relation Data

### Provider

[\[JSON Schema\]](./schemas/provider.json)

- Exposes all scrape jobs the requirer should scrape metrics through. Should be placed in the **application** databag.
- Exposes the unit address of each unit to scrape, as well as the unit name of each address. Should be placed in the **unit** databag of each scrapable unit.

#### Example


```yaml
application-data:
  alert_rules: {
    "groups": [
      {
        "name": "an_alert_rule_group",
        "rules": [
          {
            "alert": "SomethingIsUp",
            "expr": "something_bad == 1",
            "for": "0m",
            "labels": {
              "some-label": "some-value"
            },
            "annotations": {
              "some-annotation": "some-other-value"
            }
          }
        ]
      }
    ]
  }
  scrape_jobs: [
    {
      "metrics_path": "/metrics",
      "static_configs": [
        { "targets": ["*:4080"] }
      ]
    }
  ]
  scrape_metadata: {
    "model": "cos",
    "model_uuid": "c2e9f4d5-dcb3-4870-8509-330eb9745ee8",
    "application": "zinc-k8s",
    "unit": "zinc-k8s/0",
    "charm_name": "zinc-k8s"
  }
related-units:
  zinc-k8s/0:
    data:
      prometheus_scrape_unit_address: zinc-k8s-0.zinc-k8s-endpoints.cos.svc.cluster.local
      prometheus_scrape_unit_name: zinc-k8s/0
      # ...
    # ...
  zinc-k8s/1:
    data:
      prometheus_scrape_unit_address: zinc-k8s-1.zinc-k8s-endpoints.cos.svc.cluster.local
      prometheus_scrape_unit_name: zinc-k8s/1
      # ...
    # ...
```

### Requirer

No relation data should be exposed by the requirer of this relation.
