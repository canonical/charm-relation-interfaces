import dataclasses
import logging
import tempfile
from collections import defaultdict
from contextlib import contextmanager
from pathlib import Path
from subprocess import Popen, PIPE
from typing import Literal, List, NamedTuple, TYPE_CHECKING

import requests

from interface_test import run_test_case
from plugin.collect_interface_tests import collect_tests
from pytest_interface_tester import InterfaceTester

if TYPE_CHECKING:
    from plugin.collect_interface_tests import _CharmTestConfig  # noqa

logger = logging.getLogger(__file__)

ROOT = Path(__file__).parent.parent
_ROLES = Literal['requirer', 'provider']


class TestCase(NamedTuple):
    interface: str
    version: str
    role: _ROLES


def _fetch_charm_repo(path: Path, charm: "_CharmTestConfig"):
    repo_url = charm.url
    if not repo_url:
        logger.info('attempting to fetch repo url from charmhub')
        try:
            resp = requests.get(f'https://api.charmhub.io/v2/charms/info/{charm}?fields=result')
            repo_url = resp.json()['result']['website']
        except (KeyError, requests.RequestException) as e:
            raise RuntimeError(f'could not fetch charm repo info from charmhub for {charm}: '
                               f'please provide it manually') from e

    _clone_charm_repo(path, repo_url, charm.branch)


def _clone_charm_repo(path: Path, repo_url: str, branch: str = None):
    branch_opt = " --branch {branch}" if branch else ""
    cmd = f"git clone --depth 1{branch_opt} {repo_url}".split(" ")
    proc = Popen(cmd, cwd=str(path), stderr=PIPE, stdout=PIPE)
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f'failed to fetch {repo_url}:{branch}, '
                           f'check that the ref is correct. '
                           f'out={proc.stdout.read()}'
                           f'err={proc.stderr.read()}')


class LocalInterfaceTester: # todo find better name
    def __init__(self, root: Path = ROOT, include: str = "*"):
        self._root = root
        self._include = include

    def run(self):
        """Run the interface tests on all interfaces.

        First it collects the tests
        """
        tests = collect_tests(self._root, include=self._include)

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
            self._run_tests(charm, test_cases)

    @contextmanager
    def _fetch_charm(self, charm: "_CharmTestConfig"):
        with tempfile.TemporaryDirectory() as tempdir:
            temppath = Path(tempdir)
            logger.info('Fetching charm repo...')
            _fetch_charm_repo(temppath, charm)
            yield temppath

    def _run_tests(self, charm:"_CharmTestConfig", test_cases: List[TestCase]):
        with self._fetch_charm(charm) as charm_dir:
            itester: InterfaceTester = self._fetch_interface_tester_fixture(charm_dir, charm)
            for interface, version, role in test_cases:
                itester.configure(interface_version=version,
                                  interface_name=interface)
                out = run_test_case(
                    test=test,
                    schema=schema,
                    event=event,
                    state=state,
                    interface_name=interface,
                    charm_type=charm,
                    meta=self.meta,
                    config=self.config,
                    actions=self.actions,
                )


if __name__ == '__main__':
    LocalInterfaceTester().run()
