# Copyright 2023 Canonical
# See LICENSE file for licensing details.
import logging
from pathlib import Path
from typing import Type

import pydantic
from interface_tester.collector import get_schemas

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)

ROOT = Path(__file__).parent.parent
JSON_SCHEMAS_ROOT = ROOT / "docs" / "json_schemas"


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
    for role, schema_cls in get_schemas(schema_path).items():
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
