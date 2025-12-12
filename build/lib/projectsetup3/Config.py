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

    Fonts: Path = BASE / "Fonts" if os.path.exists(BASE/ "Fonts") else None

    @staticmethod
    def dispatch_path(typeProject:str) -> Path:
        if typeProject.lower() == "web":
            return Path(Config.DIRETORIO_WEB)
        elif typeProject.lower() == "cpp":
            return Path(Config.DIRETORIO_CPP)
        return Path(Config.DIRETORIO)
