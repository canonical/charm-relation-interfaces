# `s3`

## Usage

This relation interface describes the expected behaviour of any charm claiming to be able to interact with AWS S3 object storage protocol.
This relation interface should be used for all S3 protocol compatible providers, including AWS S3, MinIO, Ceph or Rook.
This interface will be accomplished using the provider library, although charm developers are free to provide alternative libraries as long as they fulfil the behavioural and schematic requirements described in this document.

## Direction

```mermaid
flowchart TD
    Provider -- bucket, access-key, secret-key, etc --> Requirer
```

As with all Juju relations, the `s3` interface consists of two parties: a Provider (object storage charm) and a Requirer (application charm). The Provider will be expected to provide new unique credentials (along with `endpoint`, `container`, `prefix` and other fields), which can be used to access the actual object storage.

## Behaviour

Both the Requirer and the Provider must adhere to criteria to be compatible with this interface.

### Provider
- It is expected to share `bucket`, `access-key` and `secret-key` fields when the relation is joined.
- It is expected to share an optional `endpoint` field containing a URL.
- It is expected to share an optional `region` field for Region.
- It is expected to share an optional `s3-uri-style` field for (S3 protocol specific) bucket path lookup. The field can take only `host` and `path` values.
- It is expected to share an optional `storage-class` field for the S3 storage class.
- It is expected to share an optional `tls-ca-chain` field for TLS verification. This field is shared by the provider if the S3 cloud has enforced TLS with custom CA certificate and can take a list of strings. Each string should be in base64 form and represent one certificate. All certificates together should represent a complete CA chain which can be used for HTTPS validation.
- It is expected to share an optional `s3-api-version` field for the (S3 protocol specific) API signature. The field can take only `2` and `4` values.
- It is expected to share an optional `attributes` field for the custom metadata. The field can take a list of strings. Server-Side-Encryption headers should be passed into this field, if any.

### Requirer
- Is expected to share a bucket name in the `bucket` field. Field value should be generated on Requirer side if no particular value set in Requirer juju config.
- Is expected to tolerate that the Provider may ignore the `bucket` field in some cases (e.g. S3Proxy or S3 Integrator) and instead use the bucket name received.
- Is expected to allow multiple different Juju applications to access the same bucket name.
- Is expected to have unique credentials for each relation. Therefore, different instances of the same Charm (juju applications) will have different relations with different credentials.
- Is expected to have different relations with different instances of the Provider if the Requirer needs access to multiple buckets.

## Relation Data

### Provider

[\[JSON Schema\]](./schemas/provider.json)

The Provider shares credentials, endpoints, TLS info and database-specific fields. It should be placed in the **application** databag.


#### Example
```yaml
  relation-info:
  - endpoint: object
    related-endpoint: object
    application-data:
      bucket: minio
      access-key: RANDOM
      secret-key: RANDOM
      path: relation-68
      endpoint: https://minio-endpoint/
      region: us-east-1
      s3-uri-style: path
      storage-class: glacier
      tls-ca-chain: base64-encoded-ca-chain==
      s3-api-version: 4
      attributes: Cache-Control=max-age=90000,min-fresh=9000;X-Amz-Server-Side-Encryption-Customer-Key=CuStoMerKey=
```

### Requirer

[\[JSON Schema\]](./schemas/requirer.json)

The Requirer shares the bucket name. It should be placed in the **application** databag.

#### Example

```yaml
  relation-info:
  - endpoint: object
    related-endpoint: object
    application-data:
      bucket: myappA
```
