from dataclasses import dataclass
import os
import json
from pathlib import Path
from projectsetup3.Config import Config
import re

@dataclass
class BaseProject:
    language = None
    basestruture:dict | None = None

    def create(self,path:Path,name:str):
        # Try exec the open json for set value.
        if self.basestruture is None:
            try:
                self.openBaseCodeJson()
            except Exception as e:
                raise RuntimeError(f"Base structure not available and couldn't be loaded: {e}")
            
        project_path = path / name
        project_path.mkdir(parents=True, exist_ok=True)

        for file, code in self.basestruture.items():
            full_path = project_path / file

            if not re.match(r".+\..+$", str(full_path)):
                full_path.mkdir(parents=True, exist_ok=True)
                continue

            full_path.parent.mkdir(parents=True, exist_ok=True)

            with full_path.open("w", encoding="UTF-8") as fileInProject:
                fileInProject.write(code)
            
    def openBaseCodeJson(self) -> None:
        if not os.path.exists(Config.basesCodesPath):
            raise ModuleNotFoundError("Diretory of base codes in json files not found")
            
        projectPath: Path = Config.basesCodesPath / f"{self.language.name.lower()}.json"

        if not os.path.isfile(projectPath):
            raise FileNotFoundError(f"Json file of {self.language.value} not found")
        
        with open(projectPath,"r+",encoding="UTF-8") as file:
            self.basestruture = json.load(file)
        