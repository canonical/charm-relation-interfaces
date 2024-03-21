# `kubernetes_manifest/v0`

## Usage

This relation interface describes the expected behavior of any charm claiming to be able to provide 
or consume the `kubernetes_manifest` interface.  `kubernetes_manifest` is an interface for sharing Kuberentes manifests sent by the requirer to the provider. 

## Behavior

### Provider

- Is expected to read the Kubernetes manifests and apply a Kubernetes object for each manifest sent by the `requirer` over the relation.  

### Requirer

- Is expected to send zero or more Kubernetes manifests to the `provider` in the below-defined format.

## Relation Data

[\[Pydantic Schema\]](./schema.py)

### Requirer

The requirer specifies zero or more manifest items in the required format.

#### Example
[
   {
      "apiVersion":"v1",
      "kind":"Secret",
      "metadata":{
         "name":"seldon-rclone-secret",
         "labels":{
            "user.kubeflow.org/enabled":"true"
         }
      },
      "stringData":{
         "RCLONE_CONFIG_MYS3_TYPE":"test"
      }
   },
   {
      "apiVersion":"v1",
      "kind":"Secret",
      "metadata":{
         "name":"mlpipeline-minio-artifact",
         "labels":{
            "user.kubeflow.org/enabled":"true"
         }
      },
      "stringData":{
         "AWS_ACCESS_KEY_ID":"access_key"
      }
   }
]
```

### Provider

The `provider` sends no data on this interface.