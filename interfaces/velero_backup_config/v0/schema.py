from interface_tester.schema_base import DataBagSchema
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class BackupSpec(BaseModel):
    """Pydantic model for the backup specification details."""
    include_namespaces: Optional[List[str]] = Field(
        None,
        alias="include-namespaces",
        description="List of namespaces to include in the backup (None means all namespaces).",
        title="Included Namespaces",
        examples=[["kubeflow"]]
    )
    include_resources: Optional[List[str]] = Field(
        None,
        alias="include-resources",
        description="List of resource kinds to include (None means all resource types).",
        title="Included Resources",
        examples=[["profiles.kubeflow.org", "deployments"]]
    )
    exclude_namespaces: Optional[List[str]] = Field(
        None,
        alias="exclude-namespaces",
        description="List of namespaces to exclude from the backup.",
        title="Excluded Namespaces",
        examples=[["default"]]
    )
    exclude_resources: Optional[List[str]] = Field(
        None,
        alias="exclude-resources",
        description="List of resource kinds to exclude from the backup.",
        title="Excluded Resources",
        examples=[["pods"]]
    )
    include_cluster_resources: bool = Field(
        False,
        alias="include-cluster-resources",
        description="Whether to include cluster-scoped resources in the backup.",
        title="Include Cluster Resources",
        examples=[True]
    )
    label_selector: Optional[Dict[str, str]] = Field(
        None,
        alias="label-selector",
        description="Label selector to filter resources for backup (e.g. {'app': 'kubeflow'}).",
        title="Label Selector",
        examples=[{"app": "kubeflow"}]
    )
    ttl: Optional[str] = Field(
        None,
        description="Optional TTL (time-to-live) for the backup (e.g. '72h' or '30d').",
        title="Backup TTL",
        examples=["24h"]
    )

class VeleroBackupSpec(BaseModel):
    """Pydantic model for the requirer's application databag."""
    app: str = Field(
        ...,
        description="Name of the client application requesting backup.",
        title="Client Application Name",
        examples=["kubeflow"]
    )
    relation_name: str = Field(
        ...,
        description="Name of the relation on the client providing this spec.",
        title="Client Relation Name",
        examples=["profiles-backup"]
    )
    spec: BackupSpec = Field(
        ...,
        description="Backup specification details (namespaces, resources, etc.).",
        title="Velero Backup Spec"
    )

class RequirerSchema(DataBagSchema):
    """Schema for the requirer (client) side of velero-backup-config."""
    app: VeleroBackupSpec  # application data uses the VeleroBackupSpec model
    # no 'unit' field, as the requirer does not use unit-level data

class ProviderSchema(DataBagSchema):
    """Schema for the provider (Velero Operator) side of velero-backup-config."""
    # The provider sends no data, so no app or unit fields are defined.
    pass
