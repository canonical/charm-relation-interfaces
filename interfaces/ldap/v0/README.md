# `ldap`

## Usage

This relation interface describes the expected behavior of any charm claiming to
be able to provide or consume the LDAP authentication configuration data.

## Glossary of LDAP Terms

| Abbreviation |            Term            |
|:------------:|:--------------------------:|
|      DN      |     Distinguished Name     |
|     DIT      | Directory Information Tree |

## Direction

```mermaid
flowchart TD
    Requirer -- user, \ngroup --> Provider
    Provider -- urls, \nbase_dn, \nbind_dn, \nbind_password_secret, \nauth_method, \nstarttls --> Requirer
```

## Behavior

Both the `provider` and the `requirer` need to adhere to a certain set of
criteria to be considered compatible with the `ldap` interface.

Sensitive information is transmitted through Juju Secrets rather than directly
through the relation databag(s).

### Provider

- Is expected to use `user` and `group` provided by the `requirer` to create a
  bind DN in the DIT for the `requirer` to use for the `bind` operation. If
  the `requirer` does not provide `user` and `group`, the `provider`
  leverages `requirer`'s Juju application name and model name.
- Is expected to provide the `requirer` with necessary configuration for
  performing LDAP authentications and operations.
- Is expected to update the application databag if any field's data is changed
  in the `provider` charmed application.

### Requirer

- Is expected to optionally provide `user` and `group` for the `provider` to
  generate the bind DN.
- Is expected to consume the LDAP configuration data provided by the `provider`
  to configure the `requirer`'s charmed application.

> #### ⚠️ Use of special characters
> Try to avoid the special characters
> listed [here](https://datatracker.ietf.org/doc/html/rfc2253#section-2.4)
> for the `user` and `group` in the `requirer`'s databag.

## Relation Data

### Provider

The `provider` provides LDAP URL, base DN, and bind DN, and LDAP
authentication method for the `requirer` to connect and perform LDAP operations.
It should be placed in the **application** databag.

#### Example

```yaml
  relation-info:
    - endpoint: ldap
      related-endpoint: ldap
      application-data:
        urls: [ldap://ldap.canonical.com:3893, ldap://ldap.ubuntu.com:3893]
        base_dn: dc=canonical,dc=com
        bind_dn: cn=app,ou=model,dc=canonical,dc=com
        bind_password_secret: secret://59060ecc-0495-4a80-8006-5f1fc13fd783/cjqub6vubg2s77p3nio0
        auth_method: simple
        starttls: true
``````

### Requirer

The `requirer` provides LDAP client information. It should be placed in the
**application** databag.

#### Example

```yaml
  relation-info:
    - endpoint: ldap
      related-endpoint: ldap
      application-data:
        user: sssd
        group: machine-localhost
```
