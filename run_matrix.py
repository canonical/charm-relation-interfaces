# Copyright 2022 Caonical Ltd.
# See LICENSE file for licensing details.

from interface_tester.collector import _CharmTestConfig, collect_tests
from pathlib import Path
import os
import shutil
import logging

FIXTURE_PATH = "tests/interface/conftest.py"
FIXTURE_IDENTIFIER = "interface_tester"
logging.getLogger().setLevel(logging.INFO)


def prepare_repo(charm_config: _CharmTestConfig, interface: str, root: Path = Path("/tmp/relation-interfaces-tests/")):
    # Clone the charm repository and create the venv if it hasn't been done already
    charm_path = root / Path(charm_config.name)
    if not charm_path.is_dir():
        branch_option = f"--branch {charm_config.branch}" if charm_config.branch is not None else ""
        os.system(f"git clone --quiet --depth 1 {branch_option} {charm_config.url} {charm_path} >/dev/null")
        _prepare_venv(charm_path)
    fixture_path, fixture_id = _get_fixture(charm_config, charm_path)
    if not fixture_path.is_file():
        raise Exception(f"Fixture missing for charm {charm_config.name}")
    test_path = _generate_test(interface, fixture_path.parent, fixture_id)
    return charm_path, test_path


def _clean(root: Path = Path("/tmp/relation-interfaces-tests/")):
    if root.is_dir():
        shutil.rmtree(root)


def _generate_test(interface: str, test_path: Path, fixture_id: str) -> Path:
    test_content = f"""from interface_tester import InterfaceTester
    
def test_{interface}_interface({fixture_id}: InterfaceTester):
    {fixture_id}.configure(
        interface_name="{interface}",
    )
    {fixture_id}.run()
    """
    test_filename = f"interface-test-{interface}.py"
    with open(test_path / test_filename, "w") as file:
        file.write(test_content)
    return test_path / test_filename
        

def _get_fixture(charm_config: _CharmTestConfig, charm_path: Path):
    fixture_path = charm_path / FIXTURE_PATH
    fixture_id = FIXTURE_IDENTIFIER
    if charm_config.test_setup:
        if charm_config.test_setup["location"]:
            fixture_path = charm_path / Path(charm_config.test_setup["location"])
        if charm_config.test_setup["identifier"]:
            fixture_id = charm_config.test_setup["identifier"]
    return fixture_path, fixture_id


def _prepare_venv(charm_path: Path) -> Path:
    """Create the venv for a charm and return the path to its python."""
    logging.info(f"Installing dependencies in venv for {charm_path}")
    original_wd = os.getcwd()
    os.chdir(charm_path)
    # Create the venv and install the requirements
    os.system("python -m venv ./.interface-venv >/dev/null")
    os.system(".interface-venv/bin/python -m pip install setuptools pytest git+https://github.com/PietroPasotti/interface-tester-pytest@main >/dev/null 2>&1")
    os.system(".interface-venv/bin/python -m pip install -r requirements.txt >/dev/null 2>&1")
    os.chdir(original_wd)
    return charm_path / ".interface-venv/bin/python"


def test_charm(charm_path: Path, test_path: Path):
    logging.info(f"Running tests for {charm_path}")
    original_wd = os.getcwd()
    os.chdir(charm_path)
    os.system(f"PYTHONPATH=src:lib .interface-venv/bin/python -m pytest {test_path}")
    os.chdir(original_wd) 


def run_interface_tests(path: Path, include: str = "*"):
    test_results = {}
    for interface, x in collect_tests(path=path, include=include).items():
        test_results[interface] = {}
        logging.info(f"Running tests for interface: {interface}")
        for _, y in x.items():
            for role in ["provider", "requirer"]:
                test_results[interface][role] = {}
                for charm_config in y[role]["charms"]:
                    last_result = "success"
                    try:
                        logging.info(f"Charm: {charm_config.name}")   
                        charm_path, test_path = prepare_repo(charm_config, interface)
                        test_charm(charm_path, test_path)
                        logging.info(f"Finished tests for charm {charm_config.name}")
                    except Exception as e:
                        logging.warning(f"exception: {e}")
                        last_result = "failure"
                    
                    test_results[interface][role][charm_config.name] = last_result
                    logging.info(f"Result: {last_result}")

    return test_results


if __name__ == "__main__":
    _clean()
    test_results = run_interface_tests(Path("."))
    print("+++ Results +++")
    print(test_results)
