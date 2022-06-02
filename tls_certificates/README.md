# `tls-certificates`

## Usage

This relation interface describes the expected behavior of any charm claiming to be able to provide 
or consume TLS certificates.

As all Juju relations, the `tls-certificates` interface consists of a provider and a requirer. 
One of these, in this case the `provider`, will be expected to create TLS certificates where the 
`requirer` will be able to consume and use them for TLS communications.

## Behavior

Both the requirer and the provider need to adhere to a certain set of criteria to be considered 
compatible with the interface.

### On relation joined

The requirer:
- Shall provide its unit name
- Shall provide a list of certificate requests 

The Provider:
- Shall provide its CA certificate
- Shall provide its CA chain
- Shall provide certificates and private keys for each certificate request.

### On relation changed

If the requirer's data bucket changes, the provider is expected to overwrite the existing 
certificates and/or remove the pre-existing certificates from the relation data.

## Relation Data

### Requirer

[\[JSON Schema\]](./schemas/requirer.json)

The requirer specifies a set of client or server common names for which it requires certificates.

#### Example

```json
{
  "unit_name": "web-app-0",
  "cert_requests": [
    {
      "common_name": "abcd.canonical.com"
    }
  ]
}
```

### Provider

[\[JSON Schema\]](./schemas/provider.json)

The provider replies with certificates for each of the requested domain.

#### Example

```json
{
  "chain": "adefeaef",
  "ca": "aedafefewa",
  "abcd.canonical.com": {
    "key": "afaefawfawfawfaafe.key",
    "cert": "abavab.crt"
  }
}
```

## Example Implementations

### providers
  - vault
  - charm-vault-k8s

### Requirers
  - keystone
  - nova-cloud
  - cinder
  - neutron
  - glance
  - charm-ceph-dashboard
