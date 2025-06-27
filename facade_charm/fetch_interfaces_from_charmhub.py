"""Scrape charmhub to grab all interfaces for all registered charms.
"""
import asyncio
import json
import logging
from pathlib import Path

import aiohttp
import requests
import tenacity
import yaml

logger = logging.getLogger("update-endpoints")

FACADE_CHARM_ROOT = Path(__file__).parent
CH_INTERFACES_PATH = FACADE_CHARM_ROOT / 'charmhub_interfaces.yaml'


def _get_all_registered_charms():
    print('fetching store...', end="")
    resp = requests.get("https://charmhub.io/packages.json")
    print('...done')
    return resp.json()['packages']


@tenacity.retry(stop=tenacity.stop_after_attempt(10), wait=tenacity.wait_fixed(1))
async def get_endpoints(charm_name, session: aiohttp.ClientSession):
    url = f"https://charmhub.io/{charm_name}/integrations.json"
    async with session.get(url=url, timeout=4) as response:
        raw = await response.read()
        return json.loads(raw)['grouped_relations']


async def get_all_integrations(charms_pkg_info):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*(get_endpoints(charm['name'], session) for charm in charms_pkg_info))
    return ret


def _gather_interfaces(charms_pkg_info):
    logger.info(f"gathering interfaces from {len(charms_pkg_info)} charms...")
    all_integrations = asyncio.run(get_all_integrations(charms_pkg_info))

    interfaces = set()
    # discard any failed ones
    for integrations in filter(None, all_integrations):
        provides = integrations.get('provides', [])
        requires = integrations.get('requires', [])
        interfaces.update(endpoint['interface'] for endpoint in provides + requires)

    logger.info(f"gathered {len(interfaces)} interfaces")
    return interfaces


def main():
    charms_pkg_info = _get_all_registered_charms()
    interfaces = _gather_interfaces(charms_pkg_info)
    CH_INTERFACES_PATH.write_text(yaml.safe_dump({"interfaces": sorted(interfaces)}))
    print(f"done --> {CH_INTERFACES_PATH}")


if __name__ == '__main__':
    main()
