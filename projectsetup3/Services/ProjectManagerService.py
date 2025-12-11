from dataclasses import dataclass
from projectsetup3.Config import Config
from projectsetup3.modules.Interfaces.BaseProject import BaseProject
from projectsetup3.modules.Enums.ProjectType import ProjectType
from pathlib import Path
import os

@dataclass
class ProjectManagerService:
    """Serviço para gerenciar criação de projetos"""
    
    @staticmethod
    def create_project(name: str, language: str, path: Path):
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

        try:
            project = BaseProject()
            project.setLanguage(ProjectType(language))
            project.openBaseCodeJson()
            project.create(path=path, name=name)
        except Exception as e:
            print(f"[ERROR] Error creating project: {e}")
            raise

    @staticmethod
    def get_base_structure(language:str):
        if not language:
            raise ValueError("Language cannot be empty.")

        try: 
            project = BaseProject()
            project.setLanguage(ProjectType(language))
            project.openBaseCodeJson() # Not Nessesary more is safely
            return project.basestruture
        except Exception as E:
            raise RuntimeError(f"Error retrieving base structure: {E}")
        
    @staticmethod
    def list_supported_languages() -> list[str]:
        return [project_type.value for project_type in ProjectType]