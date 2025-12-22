from dataclasses import dataclass
import os
import json
from pathlib import Path
from projectsetup3.Config import Config
from projectsetup3.modules.Enums.ProjectType import ProjectType
from projectsetup3.tool import tool
import datetime
import re

@dataclass
class BaseProject:
    language = None
    basestruture:dict | None = None

    def create(self,path:Path,name:str, gitRepoLink:str | None = None):
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

            if "___PROJECTNAME__" in code:
                code = code.replace("___PROJECTNAME__",name)

            if not re.match(r".+\..+$", str(full_path)):
                full_path.mkdir(parents=True, exist_ok=True)
                continue

            full_path.parent.mkdir(parents=True, exist_ok=True)

            with full_path.open("w", encoding="UTF-8") as fileInProject:
                fileInProject.write(code)

        if Config.GitAvaliable and gitRepoLink:
            tool.init_git_repository(gitRepoLink)

        if Config.HistoryAvaliable:
            DataJsonPath = Config.baseDiretoryHistory / "history.json"
            if not os.path.exists(DataJsonPath):
                history = {"projects": []}
            else:
                with DataJsonPath.open("r", encoding="UTF-8") as f:
                    history = json.load(f)

            history["projects"].append({
                "name": name,
                "language": self.language.value if self.language else None,
                "path": str(project_path.resolve()),
                "git": bool(gitRepoLink),
                "gitRepo": gitRepoLink,
                "created_at": datetime.datetime.now().isoformat()
        })

            DataJsonPath.parent.mkdir(parents=True, exist_ok=True)
            with DataJsonPath.open("w", encoding="UTF-8") as f:
                json.dump(history, f, indent=4)

    def openBaseCodeJson(self) -> None:
        if not os.path.exists(Config.basesCodesPath):
            raise ModuleNotFoundError("Diretory of base codes in json files not found")
            
        projectPath: Path = Config.basesCodesPath / f"{self.language.name.lower()}.json"

        if not os.path.isfile(projectPath):
            raise FileNotFoundError(f"Json file of {self.language.value} not found")
        
        try:
            with open(projectPath,"r",encoding="UTF-8") as file:
                self.basestruture = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {projectPath}: {e}")

    def setLanguage(self,language:ProjectType):
        self.language = language
        