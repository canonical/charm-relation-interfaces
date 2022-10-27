# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
"""Tester charm generator template."""

import os
import shutil
import tempfile
from pathlib import Path, PosixPath
from test_cases import get_test_cases

import yaml

THIS_FOLDER = Path(__file__).parent
INTERFACES_FOLDER = (THIS_FOLDER / 'interfaces')


def generate_meta(interface: str, role: str) -> str:
    return yaml.safe_dump(
        {
            'name': f'{interface}-tester',
            'display-name': f'{interface}-tester',
            'summary': f'relation interface tester charm for the "{interface}" interface',
            'description': 'manually autogenerated by simme & pietro',
            role: {
                interface: {
                    'interface': interface,
                }
            }
        }
    )

def dump_metadata(interface: str, role: str, charm_folder: PosixPath):
    # example:
    # provides:
    #   ingress:
    #     interface: ingress
    #     description: |
    #       Provides ingress-like routing to the related Juju application, load-balancing across all units

    with (charm_folder / "metadata.yaml").open('w+') as md:
        md.write(generate_meta(interface, role))



async def _build_tester_charm(ops_test, interface: str, role: str, tempdir: Path):
        old_cwd = os.getcwd()
        os.chdir(tempdir)
        shutil.copytree((THIS_FOLDER / 'charm'), tempdir, dirs_exist_ok=True)

        # delete actions, config.yaml
        dump_metadata(
            interface=interface,
            role=role,
            charm_folder=tempdir)

        source = (INTERFACES_FOLDER / interface / 'testers' / role / 'tests.yaml')
        raw_source = source.read_text()
        data = yaml.safe_load(raw_source)

        # this is only to give an early warning
        get_test_cases(data).validate()

        charm_path: Path = (tempdir / 'src' / 'charm.py')
        charm_path.write_text(
            charm_path.read_text().replace(
                '{RELATION_NAME}', interface
            ).replace(
                '{TEST_CASES}', raw_source

            )
        )
        charm = await ops_test.build_charm(tempdir)
        os.chdir(old_cwd)
        return charm


async def is_compatible(ops_test, name_of_charm_to_test: str, interface: str, tester_role: str) -> bool:
    """ Deploy a charm representing the `tester_role` for the relation interface `interface`.

    Verify that the charm called `name_of_charm_to_test` can relate to this tester
    charm and that the interface 'works', i.e. the data being exchanged satisfies
    the specification provided by the interface itself.

    Usage:
       ```python
       def test_interface(ops_test):
           await ops_test.deploy(my_charm)
           await ops_test.config(my_charm, {'config-I-need': 42})
           assert is_compatible(ops_test, 'my_charm_under_test', 'my-interface', 'my-tester-role')
       ```
    Args:
        ops_test: the OpsTest instance used in the test
        interface: the interface name to test
        tester_role: the role assumed by the tester charm (ie either provides or requires)
        name_of_charm_to_test: the charm to relate the tester charm to

    """
    tester_name = f"{interface}-tester"
    with tempfile.TemporaryDirectory(dir=THIS_FOLDER) as tempdir_name:
        path = Path(tempdir_name)
        charm = await _build_tester_charm(
            ops_test,
            interface,
            tester_role,
            path
        )
        print(charm)
        await _deploy_tester(charm, tester_name, ops_test)
    await _relate_charms(ops_test, tester_name, name_of_charm_to_test, interface)
    #
    # TODO: this needs to take elapsed time into consideration.
    #       what is a reasonable time to wait? when do we bail?
    #       - SA 2022-06-14
    assert ops_test.model.applications[tester_name].units[0].workload_status == "active"
    assert ops_test.model.applications[name_of_charm_to_test].unit[0].agent_status == "idle"
    assert any(
      msg not in ops_test.model.applications[tester_name].units[0].workload_status_message
      for msg in ('passed', 'finished'))


async def _relate_charms(ops_test, tester_charm, charm_under_test, interface):
    await ops_test.model.add_relation(f"{tester_charm}:{interface}", charm_under_test)
    await ops_test.model.wait_for_idle(
        apps=[tester_charm, charm_under_test],
        wait_for_units=1
    )


async def _deploy_tester(charm, tester_name: str, ops_test):
    await ops_test.model.deploy(charm, application_name=tester_name)
    await ops_test.model.wait_for_idle(
        apps=[tester_name],
        wait_for_units=1
    )
