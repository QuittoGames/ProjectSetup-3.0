from dataclasses import dataclass
from projectsetup3.src.core.models.Projects.Project import Project
from projectsetup3.src.core.config.Config import Config
from projectsetup3.src.core.Services.tool import tool
from projectsetup3.src.core.models.Enums.RegistredProjectType import (
    RegistredProjectType as ProjectType,
)
from projectsetup3.src.core.Services.READMEservice import READMEService
from projectsetup3.src.core.Services.History import History as HistoryService
import re
import os
import json
import datetime
from pathlib import Path


@dataclass
class ProjectFactory:
    def create(
        self,
        project_raw: Project,
        path: Path,
        name: str,
        gitRepoLink: str | None = None,
        content: str | None = None,
    ):
        project = project_raw
        if project.getBasestruture() is None:
            raise RuntimeError("Base structure is not loaded")

        project_path = path / name
        project_path.mkdir(parents=True, exist_ok=True)

        for file, code in project.getBasestruture().items():
            full_path = project_path / file

            if Config.READMEAvaliable and content and file == "README.md":
                code = READMEService.genereteREADME(
                    content,
                    name,
                    project.getLanguage().value,
                    project.getBasestruture(),
                )

            if not re.match(r".+\..+$", str(full_path)):
                full_path.mkdir(parents=True, exist_ok=True)
                continue

            full_path.parent.mkdir(parents=True, exist_ok=True)

            with full_path.open("w", encoding="UTF-8") as fileInProject:
                fileInProject.write(code)

        if Config.GitAvaliable and gitRepoLink:
            tool.init_git_repository(gitRepoLink)

        if Config.HistoryAvaliable:
            project.add_History(
                name=name, gitRepoLink=gitRepoLink, project_path=project_path
            )

    def loadProjectConfiguration(self, project: Project) -> Project | None:
        """Carrega a configuração base do projeto a partir de um JSON.

        Levanta exceptions ao chamador:
        - ModuleNotFoundError: se o diretório de base codes não existir
        - FileNotFoundError: se o arquivo JSON do projeto não for encontrado
        - json.JSONDecodeError: se o JSON for inválido
        - OSError: erros de leitura/escrita de arquivo (permissão, disco cheio, etc.)
        """
        if not os.path.exists(Config.basesCodesPath):
            raise ModuleNotFoundError("Directory of base codes in json files not found")

        # Try first by enum name (ex: python.json)
        language = project.getLanguage()
        if language is None:
            raise ValueError(
                "Project language must be set before loading its configuration"
            )

        projectPath: Path = Config.basesCodesPath / f"{language.name.lower()}.json"

        # If not exist, try by value without the dot (ex: py.json)
        if not os.path.isfile(projectPath):
            value_name = language.value.lstrip(".")
            projectPath = Config.basesCodesPath / f"{value_name}.json"

        if not os.path.isfile(projectPath):
            raise FileNotFoundError(
                f"Json file for {language.name} "
                f"(tried: {language.name.lower()}.json) not found in {Config.basesCodesPath}"
            )

        with open(projectPath, "r", encoding="UTF-8") as file:
            project.setBasestruture(json.load(file))

        return self.setFlags(project=project)

    def setFlags(self, project: Project) -> Project:
        # Pass in basestruture for trade flag for name of project
        updated_structure = {
            file.replace("___PROJECTNAME__", project.getName()): code.replace(
                "___PROJECTNAME__", project.getName()
            )
            for file, code in project.basestruture.items()
        }
        project.basestruture = updated_structure
        return project
