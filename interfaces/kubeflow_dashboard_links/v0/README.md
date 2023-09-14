# `kubeflow-dashboard-links/v0`

## Usage

This relation interface describes the expected behavior of any charm claiming to be able to provide 
or consume the `kubeflow-dashboard-links` interface.  `kubeflow-dashboard-links` is an interface for defining links in the format needed by Kubeflow Dashboard. 

## Behavior

### Provider

- Is expected to create a link in the dashboard UI for each link entry sent by the `requirer` over the relation

### Requirer

- Is expected to send zero or more links to the `provider` in the below-defined format. 

## Relation Data

### Requirer

[\[JSON Schema\]](./schemas/requirer.json)

The requirer specifies zero or more sidebar items in the required format.

#### Example

```json
[
  {
    "text": "Some link text",
    "link": "/some-relative-link",
    "location": "menu",
    "type": "item",
    "icon": "assessment",
    "desc": "link description"
  },
  {
    "text": "Some other link text",
    "link": "/some-other-relative-link",
    "location": "quick",
    "type": "item",
    "icon": "book",
    "desc": "link description"
  }

]
```

### Provider

The `provider` sends no data on this interface.
