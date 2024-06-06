# Copyright 2024 canonical
# See LICENSE file for licensing details.

import logging
from pathlib import Path
from shutil import rmtree

import yaml

logger = logging.getLogger("update-endpoints")
FACADE_CHARM_ROOT = Path(__file__).parent
MOCKS_ROOT = FACADE_CHARM_ROOT / "mocks"
CRI_ROOT = FACADE_CHARM_ROOT.parent
INTERFACES_ROOT = CRI_ROOT / 'interfaces'

CHARMCRAFT_YAML_TEMPLATE = """name: facade
type: charm
title: Facade charm
summary: Charm meant for manual and integration testing of charm interfaces.
description: |
  A programmable charm that allows you to mock relation data.
bases:
  - build-on:
    - name: ubuntu
      channel: "22.04"
    run-on:
    - name: ubuntu
      channel: "22.04"
actions:
    update:
        description: updates all databags or the specified one
        params:
            endpoint:
                type: string
                default: ""
                description: name of the endpoint
                
    clear:
        description: clears all databags or the specified one
        params:
            endpoint:
                type: string
                default: ""
                description: name of the endpoint
                
    # set:
    #     params:
    #         app:
    #             type: boolean
    #             description: target the application databag
    #         endpoint:
    #             type: string
    #             description: name of the endpoint
    #         relation_id:
    #             type: number
    #             default: -1
    #             description: relation id    
    #         contents:
    #             type: string
    #             description: comma-separated, key=value mapping. Example: foo=bar,baz=qux
    #     description: writes to a databag
        
# requires and provides is populated by tox -e update-endpoints
"""


DATABAG_TEMPLATE = """
# databag template for {interface} {role}:
# this data will be put in the application/unit databag of any relation bound on {endpoint}

# must be str:str
app_data: 
    # foo: bar
    
# must be str:str
units_data:
    # baz: qux
"""

CUSTOM_INTERFACES = ["tempo_cluster"]


def main():
    # TODO: allow adding custom interfaces on top of those scraped from CRI/interfaces
    interfaces = [] + CUSTOM_INTERFACES

    logger.info("collecting interfaces...")

    for interface_path in INTERFACES_ROOT.glob("*"):
        interface = interface_path.name

        if interface.startswith("__"):
            logger.info(f"skipping {interface}")
            continue

        interfaces.append(interface)

    endpoints = {
        "provides": {f"provide-{intf}": {"interface": intf} for intf in interfaces},
        "requires": {f"require-{intf}": {"interface": intf} for intf in interfaces}
    }

    logger.info("writing charmcraft.yaml...")
    charmcraft_yaml = FACADE_CHARM_ROOT/'charmcraft.yaml'
    post = yaml.safe_dump(endpoints)
    charmcraft_yaml.write_text(CHARMCRAFT_YAML_TEMPLATE + post)

    logger.info("cleaning up old mocks...")
    for mock in MOCKS_ROOT.glob("*"):
        if mock.name.startswith("__"):
            logger.debug(f"skipping {mock}")
            continue
        rmtree(mock)

    logger.info("generating mocks...")
    mocks_root_provide = MOCKS_ROOT / "provide"
    mocks_root_require = MOCKS_ROOT / "require"
    mocks_root_provide.mkdir(exist_ok=True)
    mocks_root_require.mkdir(exist_ok=True)

    for intf in interfaces:
        for prefix, prefixed_path in (
                ("provide", mocks_root_provide), ("require", mocks_root_require)
        ):
            endpoint = f"{prefix}-{intf}"
            mock_path = prefixed_path / (endpoint + ".yaml")
            mock_path.write_text(DATABAG_TEMPLATE.format(
                role=prefix+"r",
                interface=intf,
                endpoint=endpoint)
            )


if __name__ == '__main__':
    main()
