# Copyright 2023 Canonical
# See LICENSE file for licensing details.

import importlib
import logging
import sys
from pathlib import Path

import pydantic

logger = logging.getLogger(__file__)
ROOT = Path(__file__).parent.parent
JSON_SCHEMAS_ROOT = ROOT / "docs" / "json_schemas"


def build_schema(schema_path: Path, interface_name: str, version:int,
                 output_location: Path = JSON_SCHEMAS_ROOT):
    """Load the schemas from schema.py, dump them to docs/json_schemas/<role>.json."""
    # so we can import without tricks
    sys.path.append(str(schema_path.parent))

    # strip .py
    module_name = str(schema_path.with_suffix("").name)
    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        logger.error(f"Failed to load module {schema_path}: {e}")
        return

    # cleanup, just in case
    sys.path.remove(str(schema_path.parent))

    some_schema_found = False
    for role, name in (("provider", "ProviderSchema"),
                       ("requirer", "RequirerSchema")):
        schema_cls = getattr(module, name, None)
        if not schema_cls:
            logger.debug(f"Failed to load {name} from {schema_path}: "
                         f"schema not defined for role: {role}.")
            continue

        if not issubclass(schema_cls, pydantic.BaseModel):
            logger.error(f"Found schema class {schema_cls} in {schema_path}; "
                         f"but it is not a DataBagSchema subclass.")
            continue

        some_schema_found = True

        version_output_loc = output_location / interface_name / f"v{version}"
        version_output_loc.mkdir(exist_ok=True, parents=True)

        json_schema_file_name = (version_output_loc / role).with_suffix('.json')

        logger.info(f'dumping jsonschema for {interface_name}.{role} in {json_schema_file_name}')
        json_schema = schema_cls.schema_json(indent=2)
        json_schema_file_name.write_text(json_schema)

    if not some_schema_found:
        logger.error(f'no schema was found in {schema_path}; '
                     f'missing ProviderSchema/RequirerSchema definitions.')


def run(include: str = "*"):
    """Build all json schemas."""
    for path in (ROOT / 'interfaces').glob(include):
        interface_name = path.name
        if interface_name == '__template__':
            continue

        for version_path in path.glob("v*"):
            try:
                version = int(version_path.name[1:])
            except (TypeError, IndexError):
                logger.error(f'unable to determine version number from path: {version_path}')
                continue

            pydantic_schema = version_path / 'schema.py'
            if pydantic_schema.exists():
                logger.info(f'found pydantic schema for interface {interface_name}/v{version}')
                build_schema(pydantic_schema, interface_name, version)
            else:
                logger.info(f'no schemas found for interface {interface_name}/v{version}; skipping...')


if __name__ == '__main__':
    run()
