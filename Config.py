from dataclasses import dataclass
from pathlib import Path
import os

@dataclass
class Config:
    modules_local = ["data","modules","Intefaces","Languages","Enums"]
    Debug:str = True

    appdata = Path(os.getenv("APPDATA"))
    basesCodesPath:Path = Path(fr"{appdata}\PROJECTSETUP-3.O\Languages")

    DIRETORIO:str = r"D:\Projects\Python"

    DIRETORIO_WEB:str = r"D:\Projects\Web"

    DIRETORIO_CPP:str = r"D:\Projects\C++"

    @staticmethod
    def dispatch_path(typeProject:str) -> Path:
        if typeProject.lower() == "web":
            return Path(Config.DIRETORIO_WEB)
        elif typeProject.lower() == "cpp":
            return Path(Config.DIRETORIO_CPP)
        return Path(Config.DIRETORIO)
