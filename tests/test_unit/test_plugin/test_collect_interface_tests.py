import importlib
import random
import string
import sys
from textwrap import dedent

import pytest
from interface_tester.collector import collect_tests
from interface_tester.interface_test import (
    InvalidTestCase,
    Role,
    check_test_case_validator_signature,
    get_interface_name_and_version,
    get_registered_test_cases,
)


def test_signature_checker_too_many_params():
    def _foo(a, b, c):
        pass

    with pytest.raises(InvalidTestCase):
        check_test_case_validator_signature(_foo)


def test_signature_checker_bad_type_annotation(caplog):
    def _foo(a: int):
        pass

    check_test_case_validator_signature(_foo)
    assert (
        "interface test case validator will receive a State as first and "
        "only positional argument." in caplog.text
    )


def test_signature_checker_too_many_opt_params():
    def _foo(a, b=2, c="a"):
        pass

    with pytest.raises(InvalidTestCase):
        check_test_case_validator_signature(_foo)


@pytest.mark.parametrize("role", list(Role))
@pytest.mark.parametrize("event", ("start", "update-status", "foo-relation-joined"))
@pytest.mark.parametrize("input_state", ("State()", "State(leader=True)"))
@pytest.mark.parametrize("intf_name", ("foo", "bar"))
@pytest.mark.parametrize("version", (0, 42))
def test_registered_test_cases_cache(
    tmp_path, role, event, input_state, intf_name, version
):
    unique_name = "".join(random.choices(string.ascii_letters + string.digits, k=16))

    # if the module name is not unique, importing it multiple times will result in royal confusion
    pth = (
        tmp_path
        / "interfaces"
        / intf_name
        / f"v{version}"
        / "interface_tests"
        / f"mytestcase_{unique_name}.py"
    )
    pth.parent.mkdir(parents=True)

    pth.write_text(
        dedent(
            f"""
from interface_tester.interface_test import interface_test_case, Role
from scenario import State

@interface_test_case(
    "{role}",
    "{event}",
    input_state={input_state},
    name="{unique_name}",
    schema='skip'
)
def foo(state_out: State):
    pass
    """
        )
    )

    collect_tests(tmp_path)
    registered = get_registered_test_cases()[(intf_name, version, role)]

    # exactly one test found with the unique name we just created
    assert len([x for x in registered if x.name == unique_name]) == 1


@pytest.mark.parametrize("intf_name", ("foo", "bar"))
@pytest.mark.parametrize("version", (0, 42))
def test_get_interface_name_and_version(tmp_path, intf_name, version):
    unique_name = "".join(random.choices(string.ascii_letters + string.digits, k=16))

    pth = (
        tmp_path
        / "interfaces"
        / intf_name
        / f"v{version}"
        / "interface_tests"
        / f"mytestcase_{unique_name}.py"
    )
    pth.parent.mkdir(parents=True)
    pth.write_text("def foo(): pass")

    # so we can import without tricks
    sys.path.append(str(pth.parent))
    module_name = str(pth.with_suffix("").name)
    module = importlib.import_module(module_name)
    # cleanup
    sys.path.pop(-1)

    foo_fn = getattr(module, "foo")
    assert get_interface_name_and_version(foo_fn) == (intf_name, version)


@pytest.mark.parametrize("intf_name", ("foo", "bar"))
@pytest.mark.parametrize("version", (0, 42))
def test_get_interface_name_and_version_raises(tmp_path, intf_name, version):
    unique_name = "".join(random.choices(string.ascii_letters + string.digits, k=16))

    pth = (
        tmp_path
        / "gibber"
        / "ish"
        / intf_name
        / f"v{version}"
        / "boots"
        / f"mytestcase_{unique_name}.py"
    )
    pth.parent.mkdir(parents=True)
    pth.write_text("def foo(): pass")

    # so we can import without tricks
    sys.path.append(str(pth.parent))
    module_name = str(pth.with_suffix("").name)
    module = importlib.import_module(module_name)
    # cleanup
    sys.path.pop(-1)

    foo_fn = getattr(module, "foo")
    with pytest.raises(InvalidTestCase):
        get_interface_name_and_version(foo_fn)
