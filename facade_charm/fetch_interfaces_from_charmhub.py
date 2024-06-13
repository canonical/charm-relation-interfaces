"""Scrape charmhub to grab all interfaces for all registered charms.
"""

import json
import logging
from pathlib import Path

import requests
import tenacity
import yaml
from tenacity import stop_after_delay

logger = logging.getLogger("update-endpoints")

FACADE_CHARM_ROOT = Path(__file__).parent
CH_INTERFACES_PATH = FACADE_CHARM_ROOT / 'charmhub_interfaces.yaml'


def _get_all_registered_charms():
    print('fetching store...')
    resp = requests.get("https://charmhub.io/packages.json")
    return resp.json()['packages']


@tenacity.retry(stop=stop_after_delay(4))
def _get_integrations(charm: str) -> dict:
    resp = requests.get(f"https://charmhub.io/{charm}/integrations.json", timeout=2)
    return resp.json()['grouped_relations']


def _gather_interfaces(charms):
    interfaces = set()
    max_n = len(charms)
    for i, charm in enumerate(charms):
        charm_name = charm['name']
        print(f'({i}/{max_n}) processing {charm_name}...', end="")
        try:
            integrations = _get_integrations(charm_name)
        except json.JSONDecodeError:
            print(" [FAILED]")
            continue

        print(" [OK]")
        provides = integrations.get('provides', [])
        requires = integrations.get('requires', [])
        interfaces.update(endpoint['interface'] for endpoint in provides + requires)

    return interfaces


def main():
    charms = _get_all_registered_charms()
    interfaces = _gather_interfaces(charms)
    CH_INTERFACES_PATH.write_text(yaml.safe_dump({"interfaces": list(interfaces)}))


if __name__ == '__main__':
    main()
