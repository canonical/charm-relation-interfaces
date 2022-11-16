# `database_backup_manager`

## Usage

This relation interface describes how a database backup manager charm would interact with a database charm. A database backup manager will enable a juju admin to:

1. backup the state of a related database to a specified storage
1. restore the state of a related data from a specified backup in storage

Initially, the backup or restore will be triggered manually against the database backup manager via an action. However, eventually, the juju admin will be able to schedule periodic backups on the database backup manager.

## Direction

```mermaid
flowchart TD
    Requirer -- job-id, job-type, storage-interface, s3-config --> Provider
    Provider -- job-id, job-type, status, storage-interface, s3-config --> Requirer
```

The interface consists of two parties: a Provider (database charm) and a Requirer (database manager charm). The Requirer will be expected to provide the relevant job details, and storage interface and its config. The provider will in turn respond with the same job details, along with the `status` of the job after it has completed (either successfully or unsucessfully). The log and backup files will be stored in the provided location within the storage config.

## Behavior

The following is the criteria that a Provider and Requirer need to adhere to be compatible with this interface.

### Provider

- Is expected to detect a change in `job-id` and run either a backup or restore based on the `job-type`.
- Is expected to only run a job when it is idle. Any job further requests after a backup/restore is started may be ignored.
- Is expected to have a locking mechanism to avoid running multiple jobs at once.
- Is expected to indicate to the Requirer the status of the current or most recently completed job via the `status` field.
- Is expected to upload the log file for the job to the `log-file` in the storage config (`s3-config`).
- Is expected to upload the backup file to the `backup-file` in the storage config (`s3-config`) if it was successful in backing up the database.
- Is expected to retrieve the backup file from the `restore-file` in the storage config (`s3-config`) if it was required to restore a backup.
- Is expected to return all valid storage config (`s3-config`) fields as a reference for future jobs.

### Requirer

- Is expected to provide a unique `job-id` and `job-type` (backup or restore).
- Is expected to pass in the `storage-interface` and corresponding storage config (like `s3-config` with `access-key`, `secret-key`, `log-file`, `backup-file` and `restore-file`) needed to either store or retrieve the backup file.
- Is expected to wait until the Provider returns a `status` of the job to relay the results to the Juju admin.

## Relation Data

### Provider

[\[JSON Schema\]](./schemas/provider.json)

Provider provides information about the job (`job-id`, `job-type` and `status`) and the relevant storage information (`storage-interface` and storage config like `s3-config`). In the case of a backup, this information will be placed in the **unit** databag of the unit that performed the backup. In the case of a restore, this information will be place in the **unit** databag of the lowest numbered unit (where the restore is performed).

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
          job-id: unique-job-id
          job-type: backup
          status: success
          storage-interface: s3
          s3-config:
            access-key: access-key
            secret-key: secret-key
            log-file: s3://bucket/mysql/2022-01-01T01:01:01.123456/logs/backup.log
            backup-file: s3://bucket/mysql/2022-01-01T01:01:01.123456/backups/mysql.backup
```

```yaml
  relation-info:
  - endpoint: database-backup-manager
    related-endpoint: database-backup-manager
    application-data: {}
    related-units:
      mysql/0:
        in-scope: true
        data:
          job-id: unique-job-id
          job-type: restore
          status: success
          storage-interface: s3
          s3-config:
            access-key: access-key
            secret-key: secret-key
            log-file: s3://bucket/mysql/2022-01-01T01:01:01.123456/logs/restore.log
            restore-file: s3://bucket/mysql/2021-01-01T01:01:01.123456/backups/mysql.backup
```

### Requirer

[\[JSON Schema\]](./schemas/requirer.json)

Requirer provides the job information (`job-id`, `job-type`), `storage-interface` and the corresponding storage data (;(like `s3-config` with `access-key`, `secret-key`, `log-file`, `backup-file` and `restore-file`) in the **application** databag of the Requirer.

#### Example

```yaml
  relation-info:
  - endpoint: database-backup-manager
    related-endpoint: database-backup-manager
    application-data:
      job-id: unique-job-id
      job-type: backup
      storage-interface: s3
      s3-config:
        access-key: access-key
        secret-key: secret-key
        log-file: s3://bucket/mysql/2022-01-01T01:01:01.123456/logs/backup.log
        backup-file: s3://bucket/mysql/2022-01-01T01:01:01.123456/backups/mysql.backup
```

```yaml
  relation-info:
  - endpoint: database-backup-manager
    related-endpoint: database-backup-manager
    application-data:
      job-id: unique-job-id
      job-type: restore
      storage-interface: s3
      s3-config:
        access-key: access-key
        secret-key: secret-key
        log-file: s3://bucket/mysql/2022-01-01T01:01:01.123456/logs/restore.log
        restore-file: s3://bucket/mysql/2021-01-01T01:01:01.123456/backups/mysql.backup
```
