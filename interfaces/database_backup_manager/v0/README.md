# `database_backup_manager`

## Usage

This relation interface describes how a database backup manager charm would interact with a database charm. A database backup manager will enable a juju admin to:

1. backup the state of a related database to a specified storage
1. restore the state of a related data from a specified backup in storage

Initially, the backup or restore will be triggered manually against the database backup manager via an action. However, eventually, the juju admin will be able to schedule periodic backups on the database backup manager.

## Direction

```mermaid
flowchart TD
    Requirer -- job-id, job-type, storage-interface, storage-config, artifact-path --> Provider
    Provider -- job-id, job-type, status, artifact-path --> Requirer
```

The interface consists of two parties: a Provider (database charm) and a Requirer (database manager charm). The Requirer will be expected to provide the relevant jobs (backups or restores) to execute. The provider will then be expected to execute these jobs and respond with their statuses.

## Behavior

The following is the criteria that a Provider and Requirer need to adhere to be compatible with this interface.

### Provider

- Is expected to detect any new jobs and run either a backup or restore based on the `job-type`.
- Is expected to run concurrent backups, but only one restore at a time.
- Is expected to have appropriate locking mechanisms to avoid running incompatible jobs concurrently (e.g. a backup and a restore).
- Is expected to indicate to the Requirer the status of the current or most recently completed job via the `status` field.
- Is expected, in the case of backups, to upload backup and log artifacts to the provided storage.
- Is expected, in the case of restores, to retrieve backup artifacts from the provided storage.

### Requirer

- Is expected to provide the appropriate storage configurations for each job.
- Is expected to relay the results of completed jobs back to the Juju admin.
- Is expected to preserve the history of completed and running jobs, but also provide a mechanism to clear the history of completed jobs.

## Relation Data

### Provider

[\[JSON Schema\]](./schemas/provider.json)

Provider (database charm) is expected to record the status of running or completed jobs in the **unit** databag of the unit that performed the job. In the case of a backup, the information will be placed in the **unit** databag of the unit that performed the backup. In the case of a restore, the information will be placed in the **unit** databag of the lowest numbered unit (where the restore is performed).

#### Example
```yaml
  relation-info:
  - endpoint: database-backup-manager
    related-endpoint: database-backup-manager
    applcation-data: {}
    related-units:
      mysql/0:
        in-scope: true
        data:
          jobs: '
            [
              {
                "job-id": "another-unique-job-id",
                "job-type": "restore",
                "status": "error"
              }
            ]
          '
      mysql/1:
        in-scope: true
        data:
          jobs: '
            [
              {
                "job-id": "unique-job-id",
                "job-type": "backup",
                "status": "success",
                "artifact-path": "/path/to/backups-and-logs/"
              }
            ]
          '
```

### Requirer

[\[JSON Schema\]](./schemas/requirer.json)

Requirer (backup manager charm) is expected to request jobs by placing them in the **application** databag.

#### Example

```yaml
  relation-info:
  - endpoint: database-backup-manager
    related-endpoint: database-backup-manager
    application-data:
      jobs: '
        [
          {
            "job-id": "unique-job-id",
            "job-type": "backup",
            "storage-interface": "s3",
            "storage-config": {
              "bucket": "my-bucket",
              "access-key": "access-key",
              "secret-key": "secret-key"
            }
          },
          {
            "job-id": "another-unique-job-id",
            "job-type": "restore",
            "storage-interface": "s3",
            "storage-config": {
              "bucket": "my-bucket",
              "access-key": "access-key",
              "secret-key": "secret-key"
            },
            "artifact-path": "/path/to/retrieve/backups/"
          }
        ]
      '
```
