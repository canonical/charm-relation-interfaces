"""Runner script to execute all interface tests."""
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.

import json
import logging
import os
import shutil
import subprocess
import textwrap
from pathlib import Path

from interface_tester.collector import _CharmTestConfig, collect_tests

FIXTURE_PATH = "tests/interface/conftest.py"
FIXTURE_IDENTIFIER = "interface_tester"
logging.getLogger().setLevel(logging.INFO)

class SetupError(Exception):
    pass

class InterfaceTestError(Exception):
    pass


def prepare_repo(
    charm_config: _CharmTestConfig,
    interface: str,
    root: Path = Path("/tmp/charm-relation-interfaces-tests/"),
):
    """Clone the charm repository and create the venv if it hasn't been done already."""
    charm_path = root / Path(charm_config.name)
    if not charm_path.is_dir():
        branch_option = ""
        if charm_config.branch:
            branch_option = f"--branch {charm_config.branch}"
            logging.warning(f"custom branch provided for {charm_config.name}; this should only be done in staging")
        subprocess.call(
            f"git clone --quiet --depth 1 {branch_option} {charm_config.url} {charm_path}",
            shell=True,
            stdout=subprocess.DEVNULL
        )
        _setup_venv(charm_path)
    fixture_path, fixture_id = _get_fixture(charm_config, charm_path)
    if not fixture_path.is_file():
        # NOTE: In the future we could probably run the tests without a fixture, assuming
        # that the charm needs no patching at all to work with scenario
        raise SetupError(f"fixture missing for charm {charm_config.name}")
    test_path = _generate_test(interface, fixture_path.parent, fixture_id)
    return charm_path, test_path


def _clean(root: Path = Path("/tmp/charm-relation-interfaces-tests/")):
    """Clean the directory used to store repos for the tests."""
    if root.is_dir():
        shutil.rmtree(root)


def _generate_test(interface: str, test_path: Path, fixture_id: str) -> Path:
    """Generate a pytest file for a given charm and interface."""
    test_content = textwrap.dedent(f"""from interface_tester import InterfaceTester
    def test_{interface}_interface({fixture_id}: InterfaceTester):
        {fixture_id}.configure(
        interface_name="{interface}",
    )
    {fixture_id}.run()
    """)
    test_filename = f"interface-test-{interface}.py"
    with open(test_path / test_filename, "w") as file:
        file.write(test_content)
    return test_path / test_filename


def _get_fixture(charm_config: _CharmTestConfig, charm_path: Path):
    """Get the tester fixture from a charm."""
    fixture_path = charm_path / FIXTURE_PATH
    fixture_id = FIXTURE_IDENTIFIER
    if charm_config.test_setup:
        if charm_config.test_setup["location"]:
            fixture_path = charm_path / Path(charm_config.test_setup["location"])
        if charm_config.test_setup["identifier"]:
            fixture_id = charm_config.test_setup["identifier"]
    return fixture_path, fixture_id


def _setup_venv(charm_path: Path) -> Path:
    """Create the venv for a charm and return the path to its python."""
    logging.info(f"Installing dependencies in venv for {charm_path}")
    original_wd = os.getcwd()
    os.chdir(charm_path)
    # Create the venv and install the requirements
    try:
        subprocess.check_call("python -m venv ./.interface-venv", shell=True, stdout=subprocess.DEVNULL)
        subprocess.check_call(
            ".interface-venv/bin/python -m pip install setuptools pytest git+https://github.com/canonical/interface-tester-pytest@main",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        subprocess.check_call(
            ".interface-venv/bin/python -m pip install -r requirements.txt",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except:
        raise SetupError("venv setup failed")
    os.chdir(original_wd)
    return charm_path / ".interface-venv/bin/python"


def test_charm(charm_path: Path, test_path: Path):
    """Run the interface test for a given charm and interface."""
    logging.info(f"Running tests for {charm_path}")
    original_wd = os.getcwd()
    os.chdir(charm_path)
    try:
        subprocess.check_call(
            f"PYTHONPATH=src:lib .interface-venv/bin/python -m pytest {test_path}",
            shell=True
        )
    except:
        raise InterfaceTestError
    os.chdir(original_wd)


def run_interface_tests(path: Path, include: str = "*", clean=True):
    """Run the tests for the specified interfaces, defaulting to all."""
    if clean:
        _clean()
    test_results = {}
    for interface, x in collect_tests(path=path, include=include).items():
        test_results[interface] = {}
        logging.info(f"Running tests for interface: {interface}")
        for _, y in x.items():
            for role in ["provider", "requirer"]:
                test_results[interface][role] = {}
                for charm_config in y[role]["charms"]:
                    last_result = "success"
                    logging.info(f"Charm: {charm_config.name}")
                    try:
                        charm_path, test_path = prepare_repo(charm_config, interface)
                        test_charm(charm_path, test_path)
                    except:
                        logging.warning(f"interface tests for {charm_config.name} {interface} {role} failed", exc_info=True)
                        last_result = "failure"

                    test_results[interface][role][charm_config.name] = last_result
                    logging.info(f"Result: {last_result}")

    return test_results


def pprint_interface_test_results(test_results: dict):
    print("+++ Results +++")
    print(json.dumps(test_results, indent=2))


if __name__ == "__main__":
    test_results = run_interface_tests(Path("."))
    pprint_interface_test_results(test_results)
