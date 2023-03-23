"""
This module contains logic to gather interface tests from the relation interface specifications.
It also contains a `pprint_tests` function to display a pretty-printed listing of the
collected tests. This file is executable and will run that function when invoked.

If you are contributing a relation interface specification or modifying the tests, charms, or
schemas for one, you can execute this file to ascertain that all relevant data is being gathered
correctly.
"""

import importlib
import json
import logging
import sys
from pathlib import Path
from typing import List, Optional, Tuple, Type, TypedDict, TYPE_CHECKING, Dict

import yaml

from interface_test import (
    get_registered_test_cases,
    DataBagSchema,
    Role,
    SchemaConfig,
)

if TYPE_CHECKING:
    from interface_test import _InterfaceTestCase

ROOT = Path(__file__).parent.parent.parent

logger = logging.getLogger("interface_tests_checker")

_NotFound = object()


class _TestSetup(TypedDict):
    """Charm-specific configuration for the interface tester.

    Contains information to configure the tester."""
    location: Optional[str]
    """Path to a python file, relative to the charm's git repo root, where the `identifier` 
    below can be found. If not provided defaults to "tests/interfaces/conftest.py" """

    identifier: Optional[str]
    """Name of a python identifier pointing to a pytest fixture yielding a 
    configured InterfaceTester instance. If not provided defaults to "interface_tester" """


class _CharmSpec(TypedDict):
    name: str
    """The name of the charm."""
    url: str
    """Url of a git repository where the charm source can be found."""
    test_setup:  Optional[_TestSetup]
    """Interface tester configuration. Can be left empty. All values will be defaulted."""
    branch: Optional[str]
    """Name of the git branch where to find the interface tester configuration. 
    If not provided defaults to "main". """


class _CharmsDotYamlSpec(TypedDict):
    """Specification of the `charms.yaml` file each interface/version dir should contain."""
    providers: List[_CharmSpec]
    requirers: List[_CharmSpec]


class _RoleTestSpec(TypedDict):
    """The tests, schema, and charms for a single role of a given relation interface version."""
    tests: List["_InterfaceTestCase"]
    schema: Optional[Type[DataBagSchema]]
    charms: List[_CharmSpec]


class InterfaceTestSpec(TypedDict):
    """The tests, schema, and charms for both roles of a given relation interface version."""
    provider: _RoleTestSpec
    requirer: _RoleTestSpec


def _gather_schema_for_version(
        version_dir: Path,
) -> Tuple[Optional[Type[DataBagSchema]], Optional[Type[DataBagSchema]]]:
    """Collect the interface schema from a directory containing an interface version spec."""
    schema_location = version_dir / "schema.py"

    if not schema_location.exists():
        return None, None

    # so we can import without tricks
    sys.path.append(str(version_dir))

    # strip .py
    module_name = str(schema_location.with_suffix("").name)
    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        logger.error(f"Failed to load module {schema_location}: {e}")
        return None, None

    provider_schema = getattr(module, "ProviderSchema", None)
    if provider_schema and not issubclass(provider_schema, DataBagSchema):
        raise TypeError(
            f"{version_dir}:provider_schema is not a DataBagSchema subclass"
        )

    requirer_schema = getattr(module, "RequirerSchema", None)
    if not issubclass(requirer_schema, DataBagSchema):
        raise TypeError(
            f"{version_dir}:requirer_schema is not a DataBagSchema subclass"
        )

    # remove from import search path
    sys.path.pop(-1)
    return provider_schema, requirer_schema


def _gather_charms_for_version(version_dir: Path) -> Optional[_CharmsDotYamlSpec]:
    """Attempt to read the `charms.yaml` for this version sudir; return an empty dict on failure."""
    charms_yaml = version_dir / "charms.yaml"
    if not charms_yaml.exists():
        return None
    try:
        return yaml.safe_load(charms_yaml.read_text())
    except (json.JSONDecodeError, yaml.YAMLError) as e:
        logger.error(f"failed to decode {charms_yaml}: " f"verify that it is valid: {e}")
    except FileNotFoundError as e:
        logger.error(f"not found: {e}")
    return None


def _gather_test_cases_for_version(
        version_dir: Path, interface_name: str, version: int
):
    """Collect interface test cases from a directory containing an interface version spec."""

    interface_tests_dir = version_dir / "interface_tests"

    provider_test_cases = []
    requirer_test_cases = []

    if interface_tests_dir.exists():
        # so we can import without tricks
        sys.path.append(str(interface_tests_dir))

        for possible_test_file in interface_tests_dir.glob("*.py"):
            # strip .py
            module_name = str(possible_test_file.with_suffix("").name)
            try:
                _ = importlib.import_module(module_name)
            except ImportError as e:
                logger.error(f"Failed to load module {possible_test_file}: {e}")
                continue

            cases = get_registered_test_cases()
            provider_test_cases.extend(
                cases[(interface_name, version, Role.provider)]
            )
            requirer_test_cases.extend(
                cases[(interface_name, version, Role.requirer)]
            )

        if not (requirer_test_cases or provider_test_cases):
            logger.error(f"no valid test case files found in {interface_tests_dir}")

        # remove from import search path
        sys.path.pop(-1)
    return provider_test_cases, requirer_test_cases


def gather_test_spec_for_version(
        version_dir: Path, interface_name: str, version: int
) -> InterfaceTestSpec:
    """Collect interface tests from an interface/version subdirectory.

    Given a directory containing an interface specification (conform the template),
    collect and return the interface tests for this version.
    """

    provider_test_cases, requirer_test_cases = _gather_test_cases_for_version(
        version_dir, interface_name, version
    )
    provider_schema, requirer_schema = _gather_schema_for_version(version_dir)
    charms = _gather_charms_for_version(version_dir)

    return {
        "provider": {
            "tests": provider_test_cases,
            "schema": provider_schema,
            "charms": charms.get("providers", []) if charms else [],
        },
        "requirer": {
            "tests": requirer_test_cases,
            "schema": requirer_schema,
            "charms": charms.get("requirers", []) if charms else [],
        },
    }


def _gather_tests_for_interface(interface_dir: Path, interface_name: str) -> Dict[str, InterfaceTestSpec]:
    """Collect interface tests from an interface subdirectory.

    Given a directory containing an interface specification (conform the template),
    collect and return the interface tests for each available version.
    """
    tests = {}
    for version_dir in interface_dir.glob("v*"):
        try:
            version_n = int(version_dir.name[1:])
        except TypeError:
            logger.error(
                f"Unable to parse version {version_dir.name} as an integer. Skipping..."
            )
            continue
        tests[version_dir.name] = gather_test_spec_for_version(
            version_dir, interface_name, version_n
        )
    return tests


def collect_tests(path: Path = ROOT, include: str = "*") -> Dict[str, Dict[str, InterfaceTestSpec]]:
    """Gather the test cases collected from this path.

    Returns a dict structured as follows:
    - interface name (e.g. "ingress"):
      - version name (e.g. "v2"):
        - role (e.g. "requirer"):
          - tests: [list of interface_test._InterfaceTestCase]
          - schema: <pydantic.BaseModel>
          - charms:
            - name: foo
              url: www.github.com/canonical/foo
    """
    tests = {}
    for interface_dir in (path / "interfaces").glob(include):
        interface_dir_name = interface_dir.name
        if interface_dir_name.startswith("__"):  # ignore __template__ and python-dirs
            continue  # skip
        interface_name = interface_dir_name.replace("-", "_")
        tests[interface_name] = _gather_tests_for_interface(
            interface_dir, interface_name
        )

    return tests


def pprint_tests(include="*"):
    """Pretty-print a listing of the interface tests specified in this repository."""
    tests = collect_tests(include=include)

    def pprint_case(case: "_InterfaceTestCase"):
        state = "yes" if case.input_state else "no"
        schema_config = (
            case.schema if isinstance(case.schema, SchemaConfig) else "custom"
        )
        print(
            f"      - {case.name}:: {case.event} (state={state}, schema={schema_config})"
        )

    for interface, versions in tests.items():
        if not versions:
            print(f"{interface}: <no tests>")
            print()
            continue

        print(f"{interface}:")

        for version, roles in versions.items():
            print(f"  - {version}:")

            by_role = {role: roles[role] for role in {"requirer", "provider"}}

            for role, test_spec in by_role.items():
                print(f"   - {role}:")

                tests = test_spec["tests"]
                schema = test_spec["schema"]

                for test_cls in tests:
                    pprint_case(test_cls)
                if not tests:
                    print(f"     - <no tests>")

                if schema:
                    # todo: check if unit/app are given.
                    print(f"     - schema OK")
                else:
                    print(f"     - schema NOT OK")

                charms = test_spec["charms"]
                if charms:
                    print("     - charms:")
                    for charm in charms:
                        if isinstance(charm, str):
                            print(f"       - <BADLY FORMATTED>")
                            continue

                        custom_test_setup = "yes" if charm.get("test_setup") else "no"
                        print(
                            f'       - {charm["name"]} ({charm.get("url", "NO URL")}) '
                            f"custom_test_setup={custom_test_setup}"
                        )

                else:
                    print("     - <no charms>")

        print()


if __name__ == "__main__":
    collect_tests(include="ingress")

    pprint_tests(include="*")
