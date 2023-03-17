"""
This module contains a utility function to check that the interface tests you've just written are correctly discovered
by the same algorithm we'll at some point use to generate the relation-interfaces test matrix.
"""

import importlib
import inspect
import json
import logging
import sys
from pathlib import Path
from typing import List, Optional, Tuple, Type, TypedDict

import yaml
from scenario import State

from interface_test import DataBagSchema, _InterfaceTestCase, REGISTERED_TEST_CASES, Role, SchemaConfig

ROOT = Path(__file__).parent.parent.parent

logger = logging.getLogger("interface_tests_checker")

_NotFound = object()


class _RoleTestSpec(TypedDict):
    tests: List[_InterfaceTestCase]
    schema: Optional[Type[DataBagSchema]]
    charms: List[str]


class InterfaceTestSpec(TypedDict):
    provider: _RoleTestSpec
    requirer: _RoleTestSpec


def _try_load_and_decode(file: Path, decoder, default_factory=dict):
    if not file.exists():
        return default_factory()

    try:
        return decoder(file.read_text())
    except (json.JSONDecodeError, yaml.YAMLError) as e:
        logger.error(f"failed to decode {file}: " f"verify that it is valid: {e}")
    except FileNotFoundError as e:
        logger.error(f"not found: {e}")

    return default_factory()


def _gather_schema_for_version(
        version_dir: Path,
) -> Tuple[Optional[Type[DataBagSchema]], Optional[Type[DataBagSchema]]]:
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


def _gather_charms_for_version(version_dir: Path):
    charms_yaml = version_dir / "charms.yaml"
    return _try_load_and_decode(charms_yaml, yaml.safe_load)


def _gather_test_cases_for_version(version_dir: Path, interface_name: str, version: int):
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
                module = importlib.import_module(module_name)
            except ImportError as e:
                logger.error(f"Failed to load module {possible_test_file}: {e}")
                continue

            provider_test_cases.extend(REGISTERED_TEST_CASES[(interface_name, version, Role.provider)])
            requirer_test_cases.extend(REGISTERED_TEST_CASES[(interface_name, version, Role.requirer)])

        if not (requirer_test_cases or provider_test_cases):
            logger.error(f"no valid test case files found in {interface_tests_dir}")

        # remove from import search path
        sys.path.pop(-1)
    return provider_test_cases, requirer_test_cases


def gather_test_spec_for_version(version_dir: Path, interface_name: str, version: int) -> InterfaceTestSpec:
    provider_test_cases, requirer_test_cases = _gather_test_cases_for_version(
        version_dir, interface_name, version
    )
    provider_schema, requirer_schema = _gather_schema_for_version(version_dir)
    charms = _gather_charms_for_version(version_dir)

    return {
        "provider": {
            "tests": provider_test_cases,
            "schema": provider_schema,
            "charms": charms.get("providers", []),
        },
        "requirer": {
            "tests": requirer_test_cases,
            "schema": requirer_schema,
            "charms": charms.get("requirers", []),
        },
    }


def _gather_tests_for_interface(interface_dir: Path, interface_name: str):
    tests = {}
    for version_dir in interface_dir.glob("v*"):
        try:
            version_n = int(version_dir.name[1:])
        except TypeError:
            logger.error(f'Unable to parse version {version_dir.name} as an integer. Skipping...')
            continue
        tests[version_dir.name] = gather_test_spec_for_version(version_dir, interface_name, version_n)
    return tests


def collect_tests(root: Path = ROOT, include: str = "*"):
    tests = {}
    for interface_dir in (root / "interfaces").glob(include):
        interface_dir_name = interface_dir.name
        if interface_dir_name.startswith("__"):  # ignore __template__ and python-dirs
            continue  # skip
        interface_name = interface_dir_name.replace("-", "_")
        tests[interface_name] = _gather_tests_for_interface(interface_dir, interface_name)

    return tests


def pprint_tests(include="*"):
    tests = collect_tests(include=include)

    def pprint_case(case: _InterfaceTestCase):
        state = "yes" if case.input_state else "no"
        schema_config = case.schema if isinstance(case.schema, SchemaConfig) else "custom"
        print(f"      - {case.name}:: {case.event} (state={state}, schema={schema_config})")

    for interface, versions in tests.items():
        if not versions:
            print(f"{interface}: <no tests>")
            print()
            continue

        print(f"{interface}:")

        for version, roles in versions.items():
            print(f"  - {version}:")

            by_role = {role: roles.get(role) for role in {"requirer", "provider"}}

            for role, test_spec in by_role.items():
                tests = test_spec["tests"]
                schema = test_spec["schema"]
                print(f"   - {role}:")
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
    collect_tests(include='ingress')

    pprint_tests(include="*")
