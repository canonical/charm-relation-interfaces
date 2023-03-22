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

As all Juju relations, the `cos_agent` interface consists of a provider and a requirer. In this case the `Provider` side of the relationship may provide telemetry information such as:

- `relation_name`: name of the relation that use `cos_agent` interface
- `metrics_endpoints` to be scraped
- `metrics_rules_dir`: directory that contains Prometheus style rules
- `logs_rules_dir`: directory that contains Loki style rules
- `recursive_rules_dir`: flag that indicates if these directories should be scanned recursively
- `log_slots`: snap slots to connect to for scraping logs
- `dashboard_dirs`: list of directories that contains Grafana dashboards
- `refresh_events`: list of events on which to refresh relation data.w

These parameters are optional, if some of these are not provided, dafault values will be used:

```python
relation_name: `cos-agent`
metrics_endpoints: None
metrics_rules_dir: "./src/prometheus_alert_rules"
logs_rules_dir: "./src/loki_alert_rules"
recurse_rules_dirs: False
log_slots: None
dashboard_dirs: None
refresh_events: None
```

## Behavior

Both the `Requirer` and the `Provider` need to adhere to a certain set of criterias to be considered compatible with the interface.

### Provider

- Is expected to provide one or more Prometheus scrape jobs in the relation data bag.
- Is expected to respect the metrics topology set by the requirer.
- Is expected to provide alert rules over the relation data bag.
- Is expected to add any wanted topology labels to all metrics sent to the provider.
- Is expected to provide any wanted topology label matchers as labels on every alert rule in the relation data bag.
- Is expected to be able to expose both single alert rules and alert rule groups over the relation data bag.
- Is expected to send alert rules where the contain expressions lacks Juju topology label selectors.

### Requirer
- Is expected to be able to scrape Prometheus metrics from a metrics endpoint
- Is expected to be able to ingest alert rules exposed over the relation data bag.
- Is expected to fetch the target configuration from the relation data bag.
- Is expected to inject alert rule topology labels as label matchers in alert rule expressions.
- Is expected not to inject juju_unit as a label matcher by default, but to honor it if hard-coded by the user.
- Is expected to be able to ingest both single alert rules and alert rule groups provided over the relation data bag.

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
