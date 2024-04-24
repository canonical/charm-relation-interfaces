# Copyright 2024 Canonical
# See LICENSE file for licensing details.

"""Schem validator for `interface.yaml`"""
import yaml
import glob
import re 

from enum import Enum
from typing import List, Optional
from pydantic import AnyHttpUrl, BaseModel, Field, ValidationError


class StatusEnum(str, Enum):
    draft = "draft"
    live = "live"
    retired = "retired"

class CharmEntry(BaseModel):
    name: str
    url: AnyHttpUrl

class InterfaceModel(BaseModel):
    name: str
    version: int
    internal: Optional[bool] = False
    status: StatusEnum
    requirers: List[CharmEntry]
    providers: List[CharmEntry]

class MatchError(Exception):
    pass


class Validator:
    def _read_yaml(self, file_path: str) -> dict:
        with open(file_path, 'r') as stream:
            config = yaml.safe_load(stream)
        return config


    def _get_files(self):
        return glob.glob('./interfaces/**/interface.yaml', recursive=True)
    
    def _check_match(self, file, model):
        result = re.search(r"\/([a-zA-Z0-9-_]+)\/v(\d)+\/interface\.yaml$", file)
        if not result:
            raise MatchError("invalid folder structure. should be <name>/v<version>/interface.yaml")
        if model.name != result.group(1):
            raise MatchError("name does not match folder structure")
        if model.version != int(result.group(2)):
            raise MatchError("version ({result.group(2)}) does not match folder structure")

    """Runs the validation against all interface definitions."""
    def run(self):
        files = self._get_files()
        print(f"Scanning {len(files)} interface definitions...")
        
        errors = []
        for file in files:
            try: 
                raw_interface = self._read_yaml(file)
            except yaml.errors.YAMLError:
                errors.append(f" - {file} contains invalid yaml.")
            try:
                model = InterfaceModel(**raw_interface)
                self._check_match(file, model)
            
            except MatchError as e:
                errors.append(f"- {file} {str(e)}")
            except ValidationError:
                errors.append(f"- {file} failed validation")
        
        if errors:
            exit("\nValidation completed with errors:\n" + '\n'.join(errors) + "\n")

if __name__ == "__main__":
    Validator().run()
