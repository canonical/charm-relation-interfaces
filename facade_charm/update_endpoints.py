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
CH_INTERFACES_PATH = FACADE_CHARM_ROOT / 'charmhub_interfaces.yaml'

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
            relation_id:
                type: number
                default: -1
                description: |
                    Relation ID. If not given, 
                    all relations over this endpoint will be updated.
            app_data:
                type: string
                default: ""
                description: |
                    Json-encoded application databag. 
                    If ``{}``, the databag will be cleared.            
            unit_data:
                type: string
                default: ""
                description: |
                    Json-encoded unit databag. 
                    If ``{}``, the databag will be cleared.            
            

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


def _load_custom_interfaces() -> list:
    return yaml.safe_load((FACADE_CHARM_ROOT / 'custom_interfaces.yaml').read_text())['interfaces']


def main():
    logger.info("loading custom interfaces...")
    interfaces = _load_custom_interfaces()

    logger.info("collecting built-in interfaces...")
    for interface_path in INTERFACES_ROOT.glob("*"):
        interface = interface_path.name

        if interface.startswith("__"):
            logger.info(f"skipping {interface}")
            continue

        interfaces.append(interface)

    # add interfaces from charmhub if file is found
    if CH_INTERFACES_PATH.exists():
        logger.info(f"loading from {CH_INTERFACES_PATH}...")
        interfaces.extend(yaml.safe_load(CH_INTERFACES_PATH.read_text())['interfaces'])

    def _underscore(s: str):
        return s.replace("-", "_")

    def _dunderscore(s: str):
        return s.replace("-", "__")

    deduped = set()
    for intf in interfaces:
        if '-' in intf and _underscore(intf) in deduped:
            # of will replace - with _ on event register, so we replace - with __
            # instead to avoid endpoint name conflicts at runtime,
            logger.warning(
                f"{intf} conflicts with {_underscore(intf)}: "
                f"endpoint will be named {_dunderscore(intf)} instead"
            )
            deduped.add(_dunderscore(intf))
        else:
            deduped.add(intf)

    sorted_interfaces = sorted(deduped)

    endpoints = {
        "provides": {f"provide-{intf}": {"interface": intf} for intf in sorted_interfaces},
        "requires": {f"require-{intf}": {"interface": intf} for intf in sorted_interfaces}
    }

    logger.info("writing charmcraft.yaml...")
    charmcraft_yaml = FACADE_CHARM_ROOT / 'charmcraft.yaml'
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
                role=prefix + "r",
                interface=intf,
                endpoint=endpoint)
            )


if __name__ == '__main__':
    main()
