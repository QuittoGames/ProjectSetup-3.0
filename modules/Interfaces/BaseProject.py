from dataclasses import dataclass
import os
import json
from pathlib import Path
from data import data

@dataclass
class BaseProject:
    language = None
    basestruture:dict = None
    special:bool = False

    def create(self,path:Path):
        if self.special:
            pass

        os.path.join(path.absolute())

        for file,code in self.basestruture.items():
            full_path = path / file

            if full_path.suffix == "":
                full_path.mkdir(parents=True, exist_ok=True)
                continue

            full_path.parent.mkdir(parents=True, exist_ok=True)

            with full_path.open("w", encoding="UTF-8") as fileInProject:
                fileInProject.write(code)
            
            
    @classmethod
    def openBaseCodeJson(cls) -> None:
        if not os.path.exists(data.basesCodesPath):
            raise ModuleNotFoundError("Diretory of base codes in json files not found")
            
        projectPath:Path = data.basesCodesPath / f"{cls.language.value}.json"

        if not os.path.isfile(projectPath):
            print(projectPath.absolute)
            raise FileNotFoundError(f"Json file of {cls.language.value} not found")
        
        with open(projectPath,"r+",encoding="UTF-8") as file:
            cls.basestruture = json.load(file)
            