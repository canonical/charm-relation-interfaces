import json
import logging
from pathlib import Path
from textwrap import dedent

import pydantic
import pytest

from docs.build import build_schemas_from_source, dump_json_schema


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
    foo: int = 1"""
            ),
            "RequirerSchema",
        ),
        (
            dedent(
                """import pydantic
class ProviderSchema(pydantic.BaseModel):
    foo: int = 2"""
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
    foo: int = 1
class ProviderSchema(pydantic.BaseModel):
    foo: int = 2"""
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
        f"Found object called RequirerSchema in {schema_path}; "
        f"expecting a DataBagSchema subclass, not "
    ) in caplog.text
