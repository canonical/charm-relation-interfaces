import dataclasses
import logging
import tempfile
from collections import defaultdict
from pathlib import Path
from subprocess import Popen, PIPE
from typing import Literal, List, NamedTuple

import requests

from plugin.collect_interface_tests import collect_tests

logger = logging.getLogger(__file__)

ROOT = Path(__file__).parent.parent
_ROLES = Literal['requirer', 'provider']


class TestCase(NamedTuple):
    interface: str
    version: str
    role: _ROLES


def run_interface_tests(path: Path = ROOT, include: str = "*"):
    """Run the interface tests on all interfaces.

    First it collects the tests
    """
    tests = collect_tests(path, include=include)

    # in order to avoid fetching the same charm multiple times, we map
    # the charms to the interfaces and versions they need tested
    charms_to_interfaces = defaultdict(list)

    for interface, version_specs in tests.items():
        for version, specs in version_specs.items():
            role: _ROLES
            for role in ('requirer', 'provider'):
                for charm in specs[role]['charms']:
                    charms_to_interfaces[charm].append(
                        TestCase(interface, version, role)
                    )

    for charm, test_cases in charms_to_interfaces.items():
        _run_interface_tests(charm, test_cases)


def _fetch_charm_repo(path: Path, charm: str, repo_url: str = None, branch: str = None):
    if not repo_url:
        logger.info('attempting to fetch repo url from charmhub')
        try:
            resp = requests.get(f'https://api.charmhub.io/v2/charms/info/{charm}?fields=result')
            repo_url = resp.json()['result']['website']
        except (KeyError, requests.RequestException) as e:
            raise RuntimeError(f'could not fetch charm repo info from charmhub for {charm}: '
                               f'please provide it manually') from e

    _clone_charm_repo(path, repo_url, branch)


def _clone_charm_repo(path: Path, repo: str, branch: str = None):
    branch_opt = " --branch {branch}" if branch else ""
    cmd = f"git clone --depth 1{branch_opt} {repo}".split(" ")
    proc = Popen(cmd, cwd=str(path), stderr=PIPE, stdout=PIPE)
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f'failed to fetch {repo}:{branch}, '
                           f'check that the ref is correct. '
                           f'out={proc.stdout.read()}'
                           f'err={proc.stderr.read()}')


def _run_interface_tests(charm: str, test_cases: List[TestCase],
                         repo_url: str = None, branch: str = None):
    with tempfile.TemporaryDirectory() as tempdir:
        temppath = Path(tempdir)
        logger.info('Fetching charm repo...')
        _fetch_charm_repo(temppath, charm, repo_url=repo_url, branch=branch)

        for test_case in test_cases:
            logger.info('Searching for interface tests')

            # search for interface tests. If there is a spec for a test case: run that test.
            # todo: grab test_setup from charms
            # if no interface test is found: try running the test on the charm as it is
            # (no patching, no initial_state...)


if __name__ == '__main__':
    run_interface_tests()
