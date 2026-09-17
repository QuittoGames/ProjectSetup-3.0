from dataclasses import dataclass
from projectsetup3.src.core.config.Config import Config
from projectsetup3.src.core.models.Projects.Project import Project
from projectsetup3.src.core.models.Enums.RegistredProjectType import (
    RegistredProjectType as ProjectType,
)
from projectsetup3.src.core.Services.tool import tool
from projectsetup3.src.core.Services.Engine.ProjectFactory import ProjectFactory
from pathlib import Path


@dataclass
class ProjectService:
    """Serviço para gerenciar criação de projetos"""

    def __init__(self, factory: ProjectFactory | None = None):
        self.factory = factory or ProjectFactory()

    def create_project(
        self,
        name: str,
        language: str,
        path: Path,
        gitRepoLink: str | None = None,
        content: str | None = None,
    ):
        try:
            """Cria um novo projeto usando Project"""
            if not name:
                raise ValueError("Project name cannot be empty.")

            if not language:
                raise ValueError("Language cannot be empty.")

            if path is None:
                raise ValueError("Project path must be provided.")

            if not path.exists():
                raise FileNotFoundError(f"Path does not exist: {path}")

            if not path.is_dir():
                raise NotADirectoryError(f"Path is not a directory: {path}")

            if Config.GitAvaliable and gitRepoLink and not tool.verifyURL(gitRepoLink):
                raise ValueError(f"Invalid git repository URL: {gitRepoLink}")

            project_type = ProjectService.normalize_language(language)
            project = Project(name=name, basestruture={})
            project.setLanguage(project_type)

            self.getProjectConfiguration(project=project)
            self.factory.create(
                project_raw=project,
                path=path,
                name=name,
                gitRepoLink=gitRepoLink,
                content=content,
            )
        except Exception as e:
            raise Exception(f"[ERROR] Error creating project: {e}")

    def loadProjectConfiguration(self, language: str) -> dict | None:
        try:
            if not language:
                raise ValueError("Language cannot be empty.")

            project_type = ProjectService.normalize_language(language)
            project = Project(name="", basestruture={})
            project.setLanguage(project_type)
            self.factory.loadProjectConfiguration(project=project)

            return project.getBasestruture()
        except Exception as E:
            raise RuntimeError(f"Error retrieving base structure: {E}")
        except ModuleNotFoundError as MNF:
            raise RuntimeError(f"Error in read of base structure: {MNF}")
        except FileNotFoundError as FNFE:
            raise

    def getProjectConfiguration(self, project: Project) -> Project:
        try:
            return self.factory.loadProjectConfiguration(project=project)
        except ModuleNotFoundError as MNF:
            raise RuntimeError(f"Error in read of base structure: {MNF}")
        except FileNotFoundError as FNFE:
            raise

    @staticmethod
    def list_supported_languages() -> list[str]:
        return [project_type.value for project_type in ProjectType]

    @staticmethod
    def normalize_language(language: str) -> ProjectType:
        """Normaliza string de linguagem para ProjectType enum"""
        if not language:
            raise ValueError("Language cannot be empty.")

        language = language.strip().lower()

        if language in ProjectType.__members__:
            return ProjectType[language]

        # Tenta por valor (ex: ".py", "py")
        language_with_dot = f".{language}" if not language.startswith(".") else language
        for project_type in ProjectType:
            if (
                project_type.value == language_with_dot
                or project_type.value == language
            ):
                return project_type

        raise ValueError(f"Language '{language}' not supported")
