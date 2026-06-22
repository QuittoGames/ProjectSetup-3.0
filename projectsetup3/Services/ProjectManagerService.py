from dataclasses import dataclass
from projectsetup3.Config import Config
from projectsetup3.modules.Class.BaseProject import BaseProject
from projectsetup3.modules.Enums.ProjectType import ProjectType
from projectsetup3.tool import tool
from pathlib import Path

@dataclass
class ProjectManagerService:
    """Serviço para gerenciar criação de projetos"""
    
    @staticmethod
    def create_project(name: str, language: str, path: Path, gitRepoLink:str | None = None, content:str | None = None):
        """Cria um novo projeto usando BaseProject"""
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

        try:
            project = BaseProject()
            language = ProjectManagerService.normalize_language(language)
            project.setLanguage(language)
            project.openBaseCodeJson()
            project.create(path=path, name=name, gitRepoLink=gitRepoLink, content=content)
        except Exception as e:
            print(f"[ERROR] Error creating project: {e}")
            raise

    @staticmethod
    def get_base_structure(language:str):
        if not language:
            raise ValueError("Language cannot be empty.")

        try: 
            project = BaseProject()
            project_type = ProjectManagerService.normalize_language(language)
            project.setLanguage(project_type)
            project.openBaseCodeJson()
            return project.basestruture
        except Exception as E:
            raise RuntimeError(f"Error retrieving base structure: {E}")
        
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
            if project_type.value == language_with_dot or project_type.value == language:
                return project_type
        
        raise ValueError(f"Language '{language}' not supported")