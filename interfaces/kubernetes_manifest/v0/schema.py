"""This file defines the schemas for the provider and requirer sides of the kubernetes_manifest interface.

Examples:
    RequirerSchema:
        unit: <empty>
        kubernetes_manifests: [
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
"""

from typing import List

from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel


class KubernetesManifest(BaseModel):
    """
    Representation of a Kubernetes Object sent to Kubernetes Manifests.

    Args:
        manifest_content: the content of the Kubernetes manifest file
    """

    manifest_content: str


class RequirerSchema(DataBagSchema):
    """The schema for the requirer side of kubernetes_manifest interface."""

    app: List[KubernetesManifest]
