# `login_ui_endpoints`

## Overview

This relation interface describes the expected behavior of charms claiming to be able to provide or consume an Identity Platform Login UI endpoint.

## Usage

The interface will provide publicly accessible endpoints. These endpoints include the URL intended as the default for browsers, as well as specific endpoints for the Ory Hydra and Kratos applications.

## Endpoints

The full list of endpoints provided by login_ui_endpoints provider is the following:
- consent_url
- error_url
- index_url
- login_url
- oidc_error_url
- registration_url
- default_url

## Direction

The interface will consist of a provider and a requirer. The provider is expected to supply its endpoints,
while the requirer will just read the information from the application databag. For the full list of endpoints, please refer to the Endpoints section.

```mermaid
flowchart
    Requirer ----> Provider
    Provider -- default_url, consent_url... --> Requirer
```

## Behavior

Both the requirer and the provider need to adhere to a certain set of criteria to be considered compatible with the interface:

### Provider

- Is expected to serve all above specified endpoints 
- Is expected to write the URLs to the application databag.

### Requirer

- Is expected to consume the relation data to set up integration with Identity Platform Login UI endpoint.

## Relation Data

### Provider

[\[JSON Schema\]](./schemas/provider.json)


#### Example


```json
{
  "application_data": {
    "consent_url": "http://identity-platform-login-ui-url/consent",
    "error_url": "http://identity-platform-login-ui-url/error",
    "index_url": "http://identity-platform-login-ui-url/index",
    "login_url": "http://identity-platform-login-ui-url/login",
    "oidc_error_url": "http://identity-platform-login-ui-url/oidc_error",
    "registration_url": "http://identity-platform-login-ui-url/registration",
    "default_url": "http://identity-platform-login-ui-url"
  }
}
```

### Requirer

[\[JSON Schema\]](./schemas/requirer.json)

n/a
