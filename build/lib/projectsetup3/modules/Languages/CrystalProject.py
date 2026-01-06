from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class CrystalProject(BaseProject):
    language = ProjectType.CRYSTAL
    basestruture = {}
