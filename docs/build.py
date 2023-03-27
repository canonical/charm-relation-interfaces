# Copyright 2023 Canonical
# See LICENSE file for licensing details.

import importlib
import logging
import sys
import types
from pathlib import Path
from typing import Type

import pydantic

logger = logging.getLogger(__file__)
ROOT = Path(__file__).parent.parent
JSON_SCHEMAS_ROOT = ROOT / "docs" / "json_schemas"


def get_schema_from_module(module: object, name: str) -> Type[pydantic.BaseModel]:
    """Tries to get ``name`` from ``module``, expecting to find a pydantic.BaseModel."""
    schema_cls = getattr(module, name, None)
    if not schema_cls:
        raise NameError(name)
    if not issubclass(schema_cls, pydantic.BaseModel):
        raise TypeError(type(schema_cls))
    return schema_cls


def load_schema_module(schema_path: Path) -> types.ModuleType:
    """Import the schema.py file as a python module."""
    # so we can import without tricks
    sys.path.append(str(schema_path.parent))

    # strip .py
    module_name = str(schema_path.with_suffix("").name)
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        raise
    finally:
        # cleanup, just in case
        sys.path.remove(str(schema_path.parent))

    return module


def dump_json_schema(schema_cls: Type[pydantic.BaseModel], output_location: Path):
    """Serialize pydantic schema to jsonschema and output it to file"""
    json_schema_file_name = output_location.with_suffix(".json")
    if json_schema_file_name.exists():
        logger.info(f"file {json_schema_file_name} exists; overwriting...")
    else:
        json_schema_file_name.parent.mkdir(exist_ok=True, parents=True)

    logger.info(f"dumping jsonschema for {schema_cls} to {json_schema_file_name}")
    json_schema = schema_cls.schema_json(indent=2)
    json_schema_file_name.write_text(json_schema)


def build_schemas_from_source(
    schema_path: Path,
    output_location: Path = JSON_SCHEMAS_ROOT,
):
    """Load the schemas from schema.py, dump them to docs/json_schemas/<role>.json."""

    try:
        module = load_schema_module(schema_path)
    except ImportError as e:
        logger.error(f"Failed to load module {schema_path}: {e}")
        return

    for role, name in (("provider", "ProviderSchema"), ("requirer", "RequirerSchema")):
        try:
            schema_cls = get_schema_from_module(module, name)
        except NameError:
            logger.warning(
                f"Failed to load {name} from {schema_path}: "
                f"schema not defined for role: {role}."
            )
            continue
        except TypeError as e:
            logger.error(
                f"Found object called {name!r} in {schema_path}; "
                f"expecting a DataBagSchema subclass, not {e.args[0]!r}."
            )
            continue

        # if the schema is at /path/to/interfaces/foo/v3/schema.py,
        # we take [foo, v3]
        # the output path becomes /path/to/output_location/foo/v3/{role}.json`
        output_path = output_location.joinpath(*schema_path.parts[-3:-1], role)
        dump_json_schema(schema_cls, output_location=output_path)


def run():
    """Build all json schemas."""
    for path in (ROOT / "interfaces").rglob("schema.py"):
        if "__template__" not in path.__str__():
            logger.info(f"Found schema: building {path}")
            build_schemas_from_source(path)


if __name__ == "__main__":
    run()
