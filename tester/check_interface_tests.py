"""
This module contains a utility function to check that the interface tests you've just written are correctly discovered
by the same algorithm we'll at some point use to generate the relation-interfaces test matrix.
"""

import importlib
import inspect
import logging
import sys
from pathlib import Path
from typing import List

from scenario.structs import State

ROOT = Path(__file__).parent.parent

logger = logging.getLogger('interface_tests_checker')


def _validate_test_class(cls: type):
    # protocol we need to match:
    # class InterfaceTestCase:
    #     ROLE: Literal['provider', 'requirer'] = NotImplemented
    #     EVENT: str = NotImplemented
    #     INPUT_STATE: str = State()
    #
    #     def validate(self, output_state: State):
    #         raise NotImplementedError("validate")
    #

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


def _gather_tests_for_version(interface_tests_dir: Path):
    sys.path.append(str(interface_tests_dir))

    provider_test_cases = []
    requirer_test_cases = []

    for possible_test_file in interface_tests_dir.glob('*.py'):
        try:
            module = importlib.import_module(str(possible_test_file.name.strip('.py')))
        except ImportError as e:
            logger.error(f"Failed to load module {possible_test_file}: {e}")
            continue

        test_class_names: List[str] = module.__TESTS__
        for name in test_class_names:
            cls = getattr(module, name, _NotFound)
            if cls is _NotFound:
                logger.error(f'class {name} was specified in {possible_test_file}.__TESTS__ '
                             f'but could not be found in the module namespace')
                continue
            if not isinstance(cls, type):
                logger.error(f'{name} was specified in {possible_test_file}.__TESTS__ '
                             f'but does not refer to a type')
                continue

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

    sys.path.pop(-1)
    return {'provider': provider_test_cases,
            'requirer': requirer_test_cases}


def _gather_tests_for_interface(interface_dir: Path):
    tests = {}
    for version_dir in interface_dir.glob('v*'):
        interface_tests_dir = version_dir / 'interface_tests'
        if not interface_tests_dir.exists():
            continue

        tests[version_dir.name] = _gather_tests_for_version(interface_tests_dir)
    return tests


def gather_tests(include='*'):
    tests = {

    }
    for interface_dir in (ROOT / 'interfaces').glob(include):
        if interface_dir.name == '__template__':
            continue  # skip
        tests[interface_dir.name] = _gather_tests_for_interface(interface_dir)

    return tests


def pprint_tests(include='*'):
    tests = gather_tests(include=include)

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

            for role, tests in by_role.items():
                if tests:
                    print(f'   - {role}:')
                    for module, test_cls in tests:
                        pprint_case(test_cls)
                else:
                    print(f'   - {role}: <no tests>')
        print()


if __name__ == '__main__':
    pprint_tests(include='*')
