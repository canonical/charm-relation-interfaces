
import yaml
import glob

from enum import Enum
from typing import List, Optional
from pydantic import AnyHttpUrl, BaseModel, Field

class StatusEnum(str, Enum):
    draft = "draft"
    live = "live"
    retired = "retired"

class CharmEntry(BaseModel):
    name: str
    url: AnyHttpUrl

class Interface(BaseModel):
    interface: str
    version: int
    internal: Optional[bool] = False
    status: StatusEnum
    requirers: List[CharmEntry]
    providers: List[CharmEntry]


class Validator:
    def read_yaml(self, file_path: str) -> dict:
        with open(file_path, 'r') as stream:
            config = yaml.safe_load(stream)

        return Interface(**config)

    def get_files(self):
        return glob.glob('./interfaces/**/interface.yaml', recursive=True)
    

    def run(self):
        files = self.get_files()
        print(f"Scanning {len(files)} interface definitions...")
        for file in files:
            try: 
                self.read_yaml(file)
            except:
                print(f"- {file} failed validation")
                raise

Validator().run()