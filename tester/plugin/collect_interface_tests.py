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
from typing import Type, TypedDict, List, Dict, Any

from scenario.structs import State

from interface_test import InterfaceTestCase

ROOT = Path(__file__).parent.parent.parent

logger = logging.getLogger('interface_tests_checker')


def _validate_test_class(cls: Type[InterfaceTestCase]):
    # protocol we need to match:
    # class InterfaceTestCase:
    #     ROLE: Literal['provider', 'requirer'] = NotImplemented
    #     EVENT: str = NotImplemented
    #     INPUT_STATE: Optional[str] = State()
    #
    #     def validate(self, output_state: State):
    #         raise NotImplementedError("validate")

    errors = []

    # check optional input_state
    if input_state := getattr(cls, "INPUT_STATE", None):
        assert isinstance(input_state, State)

    # check required attrs
    for attr, validator in {
        'ROLE': lambda x: isinstance(x, str),
        'EVENT': lambda x: isinstance(x, str),
        'validate': lambda x: callable(x)
    }.items():
        if not (obj := getattr(cls, attr, None)):
            errors.append(f'class does not have required attr {attr!r}')
            continue

        if not validator(obj):
            errors.append(f'class.{attr} has an invalid value ({obj!r}) (see docs)')

    # check 'validate' signature
    validate_method = getattr(cls, "validate", None)
    if validate_method:
        sig = inspect.signature(validate_method)
        if not sig.parameters.get('output_state'):
            errors.append(f"{cls}.validate expects a single 'output_state: State' argument")

    return errors


_NotFound = object()


class _RoleTestSpec(TypedDict):
    tests: List[Type]
    schema: Dict[Any, Any]

class InterfaceTestSpec(TypedDict):
    provider: _RoleTestSpec
    requirer: _RoleTestSpec


def gather_tests_for_version(version_dir: Path) -> InterfaceTestSpec:
    interface_tests_dir = version_dir / 'interface_tests'

    provider_test_cases = []
    requirer_test_cases = []

    if interface_tests_dir.exists():
        # so we can import without tricks
        sys.path.append(str(interface_tests_dir))

        for possible_test_file in interface_tests_dir.glob('*.py'):
            try:
                module = importlib.import_module(str(possible_test_file.name.strip('.py')))
            except ImportError as e:
                logger.error(f"Failed to load module {possible_test_file}: {e}")
                continue

            test_cases = InterfaceTestCase.__subclasses__()
            test_cases_in_file = [cls for cls in test_cases if inspect.getfile(cls) == str(possible_test_file)]

            for cls in test_cases_in_file:
                cls_validation_errors = _validate_test_class(cls)
                if cls_validation_errors:
                    logger.error(f"{cls} validation failed: {cls_validation_errors}")

                else:
                    if cls.ROLE == 'provider':  # noqa we validated cls: it has ROLE.
                        cases = provider_test_cases
                    else:  # "requirer"
                        cases = requirer_test_cases
                    cases.append((module, cls))

        if not (requirer_test_cases or provider_test_cases):
            logger.error(f'no valid test case files found in {interface_tests_dir}')

        # remove from import search path
        sys.path.pop(-1)

    schemas_dir = version_dir / 'schemas'
    provider_schema = {}
    requirer_schema = {}

    if schemas_dir.exists():
        try:
            provider_schema, requirer_schema = (
                json.loads((schemas_dir / f'{role}.json').read_text())
                for role in ('provider', 'requirer')
            )
        except json.JSONDecodeError as e:
            logger.error(f'failed to decode schemas in {schemas_dir}: '
                         f'verify that the schemas are valid: {e}')

    return {
        'provider': {
            'tests': provider_test_cases,
            'schema': provider_schema
        },
        'requirer': {
            'tests': requirer_test_cases,
            'schema': requirer_schema
        }
    }


def _gather_tests_for_interface(interface_dir: Path):
    tests = {}
    for version_dir in interface_dir.glob('v*'):
        tests[version_dir.name] = gather_tests_for_version(version_dir)
    return tests


def collect_tests(root: Path = ROOT, include: str = '*'):
    tests = {

    }
    for interface_dir in (root / 'interfaces').glob(include):
        interface_dir_name = interface_dir.name
        if interface_dir_name == '__template__':
            continue  # skip
        interface_name = interface_dir_name.replace('-', '_')
        tests[interface_name] = _gather_tests_for_interface(interface_dir)

    return tests


def pprint_tests(include='*'):
    tests = collect_tests(include=include)

    def pprint_case(cls: type):
        state = 'yes' if getattr(cls, "INPUT_STATE", False) else 'no'
        print(f"      - {cls.__name__}:: {cls.EVENT} (state={state})")

    for interface, versions in tests.items():
        if not versions:
            print(f'{interface}: <no tests>')
            print()
            continue

        print(f"{interface}:")

        for version, roles in versions.items():
            print(f'  - {version}:')

            by_role = {role: roles.get(role) for role in {'requirer', 'provider'}}

            for role, test_spec in by_role.items():
                tests = test_spec['tests']
                schema = test_spec['schema']
                print(f'   - {role}:')
                for module, test_cls in tests:
                    pprint_case(test_cls)
                else:
                    print(f'     - <no tests>')

                if schema:
                    print(f'     - schema OK')
                else:
                    print(f'     - schema NOT OK')

        print()


if __name__ == '__main__':
    pprint_tests(include='*')
