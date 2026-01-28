from dataclasses import dataclass
import os
import json
from pathlib import Path
from projectsetup3.Config import Config
from projectsetup3.modules.Enums.ProjectType import ProjectType
from projectsetup3.Services.READMEService import READMEService
from projectsetup3.Services.HistoryService import HistoryService
from projectsetup3.tool import tool
import datetime
import re

@dataclass
class BaseProject:
    language = None
    basestruture:dict | None = None

    def create(self,path:Path,name:str, gitRepoLink:str | None = None , content:str | None = None):
        # Try exec the open json for set value.
        if self.basestruture is None:
            try:
                self.openBaseCodeJson()
            except Exception as e:
                raise RuntimeError(f"Base structure not available and couldn't be loaded: {e}")
            
        project_path = path / name
        project_path.mkdir(parents=True, exist_ok=True)

        #Pass in basestruture for trade flag for name of project
        updated_structure = {
            file.replace("___PROJECTNAME__", name): code.replace("___PROJECTNAME__", name)
            for file, code in self.basestruture.items()
        }
        self.basestruture = updated_structure

        for file, code in self.basestruture.items():
            full_path = project_path / file

            # Gera README.md usando IA se READMEAvaliable estiver ativo e conteúdo foi fornecido
            if Config.READMEAvaliable and content and file == "README.md":
                code = READMEService.genereteREADME(content, name, self.language.value,self.basestruture)

            if not re.match(r".+\..+$", str(full_path)):
                full_path.mkdir(parents=True, exist_ok=True)
                continue

            full_path.parent.mkdir(parents=True, exist_ok=True)

            with full_path.open("w", encoding="UTF-8") as fileInProject:
                fileInProject.write(code)

        if Config.GitAvaliable and gitRepoLink:
            tool.init_git_repository(gitRepoLink)

        if Config.HistoryAvaliable:
            history = HistoryService.getHistory()
            history["projects"].append({
                "name": name,
                "language": self.language.value if self.language else None,
                "path": str(project_path.resolve()),
                "git": bool(gitRepoLink),
                "gitRepo": gitRepoLink,
                "created_at": datetime.datetime.now().isoformat()
            })

            HistoryService.run(history)

    def openBaseCodeJson(self) -> None:
        if not os.path.exists(Config.basesCodesPath):
            raise ModuleNotFoundError("Diretory of base codes in json files not found")
            
        # Tenta primeiro pelo nome do enum (ex: python.json)
        projectPath: Path = Config.basesCodesPath / f"{self.language.name.lower()}.json"

        # Se não existir, tenta pelo value sem o ponto (ex: py.json)
        if not os.path.isfile(projectPath):
            value_name = self.language.value.lstrip('.')
            projectPath = Config.basesCodesPath / f"{value_name}.json"
        
        if not os.path.isfile(projectPath):
            raise FileNotFoundError(f"Json file for {self.language.name} (tried: {self.language.name.lower()}.json) not found in {Config.basesCodesPath}")
        
        try:
            with open(projectPath,"r",encoding="UTF-8") as file:
                self.basestruture = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {projectPath}: {e}")

    def setLanguage(self,language:ProjectType):
        self.language = language
        