from dataclasses import dataclass
from projectsetup3.Config import Config
from projectsetup3.modules.DataMap.project_map import ProjectMaps
from pathlib import Path

# Yes i need to create the service for my self code

# - ProjectManagerService
#   - Intefaces Modules For Project
#    - DataMap Create

#OBS: Is possible you use the classic servicce with BaseProject Classs more is the same for you one python lib

@dataclass
class ProjectManagerService:
    @staticmethod
    def create_project(name:str, language:str,path:Path):

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
            ProjectLocal = ProjectMaps.project_map[language.lower()]()
            ProjectLocal.openBaseCodeJson() # Not Nessesary more is safely
            project_path = path if path else Config.dispatch_path(language)
            ProjectLocal.create(path=project_path,name = name)
        except Exception as E:
            print(f"[ERROR] Errro in createe the project, Erro: {E}")

    @staticmethod
    def get_base_structure(language:str):
        if not language:
            raise ValueError("Language cannot be empty.")

        try:        
            ProjectLocal = ProjectMaps.project_map[language.lower()]()
            ProjectLocal.openBaseCodeJson() # Not Nessesary more is safely
            return ProjectLocal.basestruture
        except Exception as E:
            raise RuntimeError(f"Error retrieving base structure: {E}")
        
    @staticmethod
    def list_supported_languages() -> list[str]:
        return list(ProjectMaps.project_map.keys())
    