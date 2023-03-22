import json
import logging
from pathlib import Path
from textwrap import dedent

import pydantic
import pytest

from docs.build import (
    build_schemas_from_source,
    dump_json_schema,
    get_schema_from_module,
    load_schema_module,
)


def test_load_schema_module(tmp_path):
    pth = Path(tmp_path) / "foo.py"
    pth.write_text(
        dedent(
            """
FOO = 1
        """
        )
    )

    module = load_schema_module(pth)
    assert module.FOO == 1


def test_get_schema_from_module(tmp_path):
    pth = Path(tmp_path) / "bar.py"
    pth.write_text(
        dedent(
            """
import pydantic
class RequirerSchema(pydantic.BaseModel):
    foo = 1
class ProviderSchema(pydantic.BaseModel):
    foo = 2
class Foo(pydantic.BaseModel):
    foo = 3
class Bar:
    pass
"""
        )
    )
    module = load_schema_module(pth)

    requirer_schema = get_schema_from_module(module, "RequirerSchema")
    assert requirer_schema.__fields__["foo"].default == 1
    provider_schema = get_schema_from_module(module, "ProviderSchema")
    assert provider_schema.__fields__["foo"].default == 2
    foo_schema = get_schema_from_module(module, "Foo")
    assert foo_schema.__fields__["foo"].default == 3

    # fails because it's not a pydantic model
    with pytest.raises(TypeError):
        get_schema_from_module(module, "Bar")

    # fails because it's not found in the module
    with pytest.raises(NameError):
        get_schema_from_module(module, "Baz")


def test_dump_json_schema(tmp_path):
    pth = Path(tmp_path) / "myrole"  # will be requirer/provider

    class MySchema(pydantic.BaseModel):
        foo: int = 1
        bar: str

    dump_json_schema(MySchema, pth)
    jsn = json.load(pth.with_suffix(".json").open())
    assert jsn == {
        "title": "MySchema",
        "type": "object",
        "properties": {
            "foo": {"title": "Foo", "default": 1, "type": "integer"},
            "bar": {"title": "Bar", "type": "string"},
        },
        "required": ["bar"],
    }


def test_build_schemas_from_source(tmp_path):
    pth = Path(tmp_path)
    schema_path = pth / "baz.py"

    build_schemas_from_source(
        schema_path=schema_path, interface_name="foo", version=42, output_location=pth
    )


def test_build_schemas_from_empty_source(tmp_path, caplog):
    pth = Path(tmp_path)
    schema_path = pth / "my_schema.py"
    # there is a module but it's empty
    schema_path.touch()

    with caplog.at_level(logging.DEBUG):
        build_schemas_from_source(
            schema_path=schema_path,
            interface_name="foo",
            version=42,
            output_location=pth,
        )

    assert (
        f"Failed to load RequirerSchema from {schema_path}: "
        f"schema not defined for role: requirer." in caplog.text
    )

    assert (
        f"Failed to load ProviderSchema from {schema_path}: "
        f"schema not defined for role: provider." in caplog.text
    )

    assert (
        f"no schema was found in {schema_path}; "
        f"missing ProviderSchema/RequirerSchema definitions." in caplog.text
    )


def test_build_schemas_from_nonempty_but_bad_source(tmp_path, caplog):
    pth = Path(tmp_path)
    schema_path = pth / "my_schema.py"
    # there is a module, but it's full of uninteresting stuff
    schema_path.write_text(
        dedent(
            """
import pydantic
class Foo(pydantic.BaseModel):
    pass
class Bar:
    pass
"""
        )
    )
    with caplog.at_level(logging.DEBUG):
        build_schemas_from_source(
            schema_path=schema_path,
            interface_name="foo",
            version=42,
            output_location=pth,
        )

    assert (
        f"Failed to load RequirerSchema from {schema_path}: "
        f"schema not defined for role: requirer." in caplog.text
    )

    assert (
        f"Failed to load ProviderSchema from {schema_path}: "
        f"schema not defined for role: provider." in caplog.text
    )

    assert (
        f"no schema was found in {schema_path}; "
        f"missing ProviderSchema/RequirerSchema definitions." in caplog.text
    )


@pytest.mark.parametrize(
    "source",
    (
        dedent(
            """
import pydantic
class RequirerSchema:
    pass
"""
        ),
        dedent(
            """
RequirerSchema = 42
"""
        ),
    ),
)
def test_build_schemas_broken_source(tmp_path, source, caplog):
    caplog.clear()

    pth = Path(tmp_path)
    schema_path = pth / "qux.py"
    # there is a module, but the name points to something unexpected
    schema_path.write_text(source)
    with caplog.at_level(logging.DEBUG):
        build_schemas_from_source(
            schema_path=schema_path,
            interface_name="foo",
            version=42,
            output_location=pth,
        )

    assert (
        f"Found object called 'RequirerSchema' in {schema_path}; "
        f"expecting a DataBagSchema subclass, not" in caplog.text
    )
