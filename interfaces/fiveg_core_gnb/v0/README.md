# `fiveg_core_gnb`

## Usage

Within 5G, the CU is the Central Unit of a RAN (Radio Access Network) and needs to be configured according to the 5G network parameters.

The `fiveg_core_gnb` relation interface describes the expected behavior of any charm claiming to be able to provide or consume the CU (or gNodeB) configuration information.

In a typical 5G network, the provider of this interface would be a CU or a gNodeB. The requirer of this interface would be the NMS (Network Management System).

## Direction

```mermaid
flowchart TD
    Provider -- MCC, MNC, TAC, SST, SD --> Requirer
    Requirer -- CU/gNodeB Identifier --> Provider
```

As with all Juju relations, the `fiveg_core_gnb` interface consists of two parties: a Provider and a Requirer.

## Behavior

Both the Requirer and the Provider need to adhere to criteria to be considered compatible with the interface.

### Provider

- Is expected to provide the following data:
  - TAC (Tracking Area Code)
  - List of PLMNs

The list of PLMNs should include the following data:
  - MCC (Mobile Country Code)
  - MNC (Mobile Network Code)
  - SST (Slice Service Type)
  - SD (Slice Differentiator)

TAC shall adhere to the following rules:
  - integer between 1 and 16777215

The values of each PLMN shall adhere to the following rules:
  - MCC must be a numeric string of length three
  - MNC must be a numeric string of length two or three
  - SST must be an integer between 0 and 255
  - SD must be an integer between 0 and 16777215

### Requirer

- Is expected to provide a unique identifier of the CU (or gNodeB).

The unique identifier shall adhere to the following rules:
  - only alphanumeric, underscores, dashes are allowed
  - length must be between 2 and 256 characters, with the first one being alphabetic

## Relation Data

[\[Pydantic Schema\]](./schema.py)

#### Example

```yaml
provider:
  app: {
    "tac": 1,
    "plmns": [
      {
        "mcc": "001",
        "mnc": "01",
        "sst": 1,
        "sd": 1,
      }
    ],
  }
  unit: {}
requirer:
  app: {
    "gnb-name": "gnb001"
  }
  unit: {}
```
