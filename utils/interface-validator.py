# Copyright 2024 Canonical
# See LICENSE file for licensing details.

"""Schema validator for `interface.yaml` files."""
import yaml
import glob
import re 

from enum import Enum
from typing import List, Optional
from pydantic import AnyHttpUrl, BaseModel, ValidationError, ConfigDict

class text:
   BOLD = '\033[1m'
   CYAN = '\033[96m'

   END = '\033[0m'


class StatusEnum(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RETIRED = "retired"

class TestSetup(BaseModel):
    model_config = ConfigDict(extra='forbid')

    location: Optional[str] = None
    identifier: Optional[str] = None
    charm_root: Optional[str] = None
    pre_run: Optional[str] = None

class CharmEntry(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str
    url: AnyHttpUrl
    branch: Optional[str] = None
    test_setup: Optional[TestSetup] = None

class InterfaceModel(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str
    version: int
    internal: Optional[bool] = False
    status: StatusEnum
    requirers: List[CharmEntry]
    providers: List[CharmEntry]
    maintainer: Optional[str] = ""

class MatchError(Exception):
    """Error raised when the location of an interface.yaml spec file is inconsistent with its contents."""


class Validator:
    def _read_yaml(self, file_path: str) -> dict:
        with open(file_path, 'r') as stream:
            config = yaml.safe_load(stream)
        return config


    def _get_files(self):
        return glob.glob('./interfaces/**/interface.yaml', recursive=True)
    
    def _validate_against_path(self, file, model):
        result = re.search(r"\/([a-zA-Z0-9-_]+)\/v(\d)+\/interface\.yaml$", file)
        if not result:
            raise MatchError("invalid folder structure. should be <name>/v<version>/interface.yaml")
        if model.name != result.group(1):
            raise MatchError(f"name '{model.name}' does not match folder structure '{result.group(1)}'")
        if model.version != int(result.group(2)):
            raise MatchError(f"version ({result.group(2)}) does not match folder structure")

    """Runs the validation against all interface definitions."""
    def run(self):
        files = self._get_files()
        print(f"Scanning {len(files)} interface definitions...")
        
        errors = []
        for file in files:
            try: 
                raw_interface = self._read_yaml(file)
                model = InterfaceModel(**raw_interface)
                self._validate_against_path(file, model)
            except yaml.error.YAMLError as e:
                errors.append(f"{text.BOLD + text.CYAN + file + text.END}:\n{str(e)}")
            except MatchError as e:
                errors.append(f"{text.BOLD + text.CYAN + file + text.END}:\n{str(e)}")
            except ValidationError as e:
                errors.append(f"{text.BOLD + text.CYAN + file + text.END}:\n{str(e)}")

        
        if errors:
            exit("\nValidation completed with errors:\n\n" + '\n---\n'.join(errors) + "\n")
        else:
            print("Validation completed!")

if __name__ == "__main__":
    Validator().run()
