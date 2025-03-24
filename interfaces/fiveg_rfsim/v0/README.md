# `fiveg_rfsim`

## Usage

Within 5G RAN (Radio Access Network) architecture, the OAI DU charm can be started to act as both the DU and the RU through its RF simulator functionality. 

The OAI UE charm requires RF simulator address and the network information(SST, SD) in order to connect. Hence, the provider of this interface would be a OAI DU charm and the requirer of this interface would be the OAI UE charm.

This relation interface describes the expected behavior of charms claiming to be able to provide or consume information on connectivity over the fiveg_rfsim interface.

## Direction

```mermaid
flowchart TD
    Provider -- version, rfsim_address, sst, sd, band, dl_freq, carrier_bandwidth, numerology, start_subcarrier --> Requirer
    Requirer -- version --> Provider
```

As with all Juju relations, the `fiveg_rfsim` interface consists of two parties: a Provider and a Requirer.

## Behavior

Both the Requirer and the Provider need to adhere to criteria to be considered compatible with the interface.

### Provider

Is expected to provide following information:

- Version of the interface
- The DU's `rfsim` service ip
- Network Slice/Service Type (SST)
- Slice Differentiator (SD)
- Frequency band
- Downlink frequency (in Hz)
- Carrier bandwidth (number of downlink PRBs)
- Numerology
- Start subcarrier

### Requirer

- Version of the interface
- Is expected to use the `rfsim` service address and the network information(SST, SD) passed by the provider.

## Relation Data

[\[Pydantic Schema\]](schema.py)

#### Example

```yaml
provider:
  app: {
    "version": 0,
    "rfsim_address": "192.168.70.130",
    "sst": 1,
    "sd": 1,
    "band": 77,
    "dl_freq": 4059090000,
    "carrier_bandwidth": 106,
    "numerology": 1,
    "start_subcarrier": 541,
  }
  unit: {}
requirer:
  app: {
    "version": 0,
  }
  unit: {}
```
