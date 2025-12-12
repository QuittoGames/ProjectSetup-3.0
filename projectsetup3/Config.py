from dataclasses import dataclass
from pathlib import Path
import os
import platform

@dataclass
class Config:
    modules_local = ["data","modules","Intefaces","Languages","Enums","Class"]
    Debug:str = False

    appdata = Path(os.getenv("APPDATA")) if platform.system().lower() == "windows" else Path.home() / ".config" / "ProjectSetup"
    BASE = Path(__file__).resolve().parent

    basesCodesPath: Path = appdata / "PROJECTSETUP-3.O" / "Languages"

    DIRETORIO: Path = Path("D:/Projects/Python")
    DIRETORIO_WEB: Path = Path("D:/Projects/Web")
    DIRETORIO_CPP: Path = Path("D:/Projects/C++")

    BASECODEEDITOR:str = "vscode"

    GitAvaliable:bool = False  

    Fonts: Path = BASE / "Fonts" if os.path.exists(BASE/ "Fonts") else None

    PROJECT_TYPES = {
        "Python": {
            "files": ["requirements.txt", "pyproject.toml"],
            "extensions": [".py"],
        },
        "Node/JS": {
            "files": ["package.json"],
            "extensions": [".js", ".ts", ".tsx"],
        },
        "Java": {
            "files": ["pom.xml"],
            "extensions": [".java"],
        },
        "Rust": {
            "files": ["Cargo.toml"],
            "extensions": [".rs"],
        },
        "C++": {
            "files": [],
            "extensions": [".cpp", ".cc", ".cxx", ".hpp", ".h"],
        },
        "C": {
            "files": [],
            "extensions": [".c", ".h"],
        },
        "Go": {
            "files": [],
            "extensions": [".go"],
        },
        "C#": {
            "files": [],
            "extensions": [".cs", ".csproj"],
        },
        "Ruby": {
            "files": [],
            "extensions": [".rb"],
        },
        "Lua": {
            "files": [],
            "extensions": [".lua"],
        },
        "Shell": {
            "files": [],
            "extensions": [".sh", ".bash"],
        },
        "YAML": {
            "files": [],
            "extensions": [".yaml", ".yml"],
        },
        "Web": {
            "files": [],
            "extensions": [".html", ".css"],
        },
    }

    @staticmethod
    def dispatch_path(typeProject:str) -> Path:
        if typeProject.lower() == "web":
            return Path(Config.DIRETORIO_WEB)
        elif typeProject.lower() == "cpp":
            return Path(Config.DIRETORIO_CPP)
        return Path(Config.DIRETORIO)
    
    def get_editor_link(editor: str, project_path: Path) -> str:
        editors = {
            "vscode":   f"vscode://file/{project_path}",
            "cursor":   f"cursor://file/{project_path}",
            "vscodium": f"vscodium://file/{project_path}",
            "sublime":  f"subl://open?url=file://{project_path}",
            "pycharm":  f"pycharm://open?file={project_path}",
            "idea":     f"idea://open?file={project_path}",
            "webstorm": f"webstorm://open?file={project_path}",
        }

        return editors.get(editor.lower(), f"vscode://file/{project_path}")
