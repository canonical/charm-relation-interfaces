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


@pytest.mark.parametrize(
    "module_contents, schema_name",
    (
        (
            dedent(
                """import pydantic
class RequirerSchema(pydantic.BaseModel):
    foo = 1"""
            ),
            "RequirerSchema",
        ),
        (
            dedent(
                """import pydantic
class ProviderSchema(pydantic.BaseModel):
    foo = 2"""
            ),
            "ProviderSchema",
        ),
    ),
)
def test_build_schemas_from_source_one_only(tmp_path, module_contents, schema_name):
    pth = Path(tmp_path)
    schema_output_path = pth / "outputs"
    schema_path = pth / "foo" / "v42" / f"baz_one_{schema_name}.py"
    schema_path.parent.mkdir(exist_ok=True, parents=True)

    schema_path.write_text(module_contents)
    build_schemas_from_source(
        schema_path=schema_path, output_location=schema_output_path
    )

    schema_outputs = schema_output_path / "foo" / "v42"
    if schema_name == "ProviderSchema":
        assert (schema_outputs / "provider.json").exists()
        assert not (schema_outputs / "requirer.json").exists()
    if schema_name == "RequirerSchema":
        assert not (schema_outputs / "provider.json").exists()
        assert (schema_outputs / "requirer.json").exists()


def test_build_schemas_from_source_both(tmp_path):
    pth = Path(tmp_path)
    schema_path = pth / "foo" / "v42" / "baz_both.py"
    schema_path.parent.mkdir(exist_ok=True, parents=True)

    schema_path.write_text(
        dedent(
            """import pydantic
class RequirerSchema(pydantic.BaseModel):
    foo = 1
class ProviderSchema(pydantic.BaseModel):
    foo = 2"""
        )
    )
    build_schemas_from_source(schema_path=schema_path, output_location=pth)

    schema_output_path = pth / "foo" / "v42"
    assert (schema_output_path / "provider.json").exists()
    assert (schema_output_path / "requirer.json").exists()


def test_build_schemas_from_empty_source(tmp_path, caplog):
    pth = Path(tmp_path)
    schema_path = pth / "foo" / "v42" / "my_schema.py"
    schema_path.parent.mkdir(exist_ok=True, parents=True)

    # there is a module but it's empty
    schema_path.touch()

    with caplog.at_level(logging.DEBUG):
        build_schemas_from_source(
            schema_path=schema_path,
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


def test_build_schemas_from_nonempty_but_bad_source(tmp_path, caplog):
    pth = Path(tmp_path)
    schema_path = pth / "foo" / "v42" / "my_schema.py"
    schema_path.parent.mkdir(exist_ok=True, parents=True)

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


@pytest.mark.parametrize(
    "source",
    (
        dedent(
            """import pydantic
class RequirerSchema:
    pass
        """
        ),
        dedent(
            """RequirerSchema = 42
        """
        ),
    ),
)
def test_build_schemas_broken_source(tmp_path, source, caplog):
    caplog.clear()

    pth = Path(tmp_path)
    schema_path = pth / "foo" / "v42" / "qux.py"
    schema_path.parent.mkdir(exist_ok=True, parents=True)

    # there is a module, but the name points to something unexpected
    schema_path.write_text(source)
    with caplog.at_level(logging.DEBUG):
        build_schemas_from_source(
            schema_path=schema_path,
            output_location=pth,
        )

    assert (
        f"Found object called 'RequirerSchema' in {schema_path}; "
        f"expecting a DataBagSchema subclass, not" in caplog.text
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


@pytest.mark.parametrize(
    "module_contents, schema_name, foo_value",
    (
        (
            dedent(
                """import pydantic
class RequirerSchema(pydantic.BaseModel):
    foo = 1"""
            ),
            "RequirerSchema",
            1,
        ),
        (
            dedent(
                """import pydantic
class ProviderSchema(pydantic.BaseModel):
    foo = 2"""
            ),
            "ProviderSchema",
            2,
        ),
        (
            dedent(
                """import pydantic
class Foo(pydantic.BaseModel):
    foo = 3"""
            ),
            "Foo",
            3,
        ),
    ),
)
def test_get_schema_from_module(tmp_path, module_contents, schema_name, foo_value):
    # unique filename else it will load the wrong module
    pth = Path(tmp_path) / f"bar{schema_name}.py"
    pth.write_text(module_contents)
    module = load_schema_module(pth)

    requirer_schema = get_schema_from_module(module, schema_name)
    assert requirer_schema.__fields__["foo"].default == foo_value


@pytest.mark.parametrize(
    "module_contents, schema_name",
    (
        (dedent("""Foo2=1"""), "Foo2"),
        (dedent("""Bar='baz'"""), "Bar"),
        (dedent("""Baz=[1,2,3]"""), "Baz"),
    ),
)
def test_get_schema_from_module_wrong_type(tmp_path, module_contents, schema_name):
    # unique filename else it will load the wrong module
    pth = Path(tmp_path) / f"bar{schema_name}.py"
    pth.write_text(module_contents)
    module = load_schema_module(pth)

    # fails because it's not a pydantic model
    with pytest.raises(TypeError):
        get_schema_from_module(module, schema_name)


@pytest.mark.parametrize("schema_name", ("foo", "bar", "baz"))
def test_get_schema_from_module_bad_name(tmp_path, schema_name):
    pth = Path(tmp_path) / "bar3.py"
    pth.write_text("dead='beef'")
    module = load_schema_module(pth)

    # fails because it's not found in the module
    with pytest.raises(NameError):
        get_schema_from_module(module, schema_name)
