from interface_tester import Tester
from scenario import State, Relation

def test_no_data_on_created():
    t = Tester()
    state_out = t.run("profiles-backup-relation-created")
    t.assert_relation_data_empty()

def test_no_data_on_joined():
    t = Tester()
    state_out = t.run("profiles-backup-relation-joined")
    t.assert_schema_valid()

def test_no_data_on_changed():
    t = Tester()
    state_out = t.run("profiles-backup-relation-changed")
    t.assert_schema_valid()

def test_data_written_happy_path():
    # GIVEN that the remote end has requested a container in the right format
    t = Tester(
        State(
            leader=True,
            relations=[
                Relation(
                    endpoint="profiles-backup",
                    interface="velero_backup_config",
                    remote_app_data={
                        "app": "velero-kubeflow",
                        "relation_name": "profiles-backup",
                        "spec": {
                            "include_namespaces": ["kubeflow"],
                            "include_resources": ["profiles.kubeflow.org"],
                            "label_selector": { "app": "kubeflow" },
                            "ttl": "24h",
                        },
                    },
                )
            ],
        )
    )
    # WHEN this charm receives a relation-changed event
    state_out = t.run("profiles-backup-relation-changed")

    # THEN the schema is satisfied (this charm published all required fields)
    t.assert_schema_valid()
