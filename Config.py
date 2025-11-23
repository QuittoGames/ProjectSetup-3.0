from dataclasses import dataclass
from pathlib import Path
import os

@dataclass
class Config:
    modules_local = ["data","modules","Intefaces","Languages","Enums"]
    Debug:str = False

    appdata = Path(os.getenv("APPDATA"))
    basesCodesPath:Path = Path(fr"{appdata}\PROJECTSETUP-3.O\Languages")