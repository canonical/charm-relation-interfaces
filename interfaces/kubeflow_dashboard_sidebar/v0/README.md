# `kubeflow-dashboard-sidebar/v0`

## Usage

This relation interface describes the expected behavior of any charm claiming to be able to provide 
or consume the `kubeflow-dashboard-sidebar`.  `kubeflow-dashboard-sidebar` is an interface for defining links in the format of Kubeflow Dashboard's sidebar. 

## Behavior

### Provider

- Is expected to create a sidebar link in the dashboard UI for each link entry sent by the `requirer` over the relation

### Requirer

- Is expected to send zero or more sidebar items to the `provider` in the below-defined format. 

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
    "type": "item",
    "icon": "assessment"
  },
  {
    "text": "Some other link text",
    "link": "/some-other-relative-link",
    "type": "item",
    "icon": "book"
  }

]
```

### Provider

The `provider` sends no data on this interface.
