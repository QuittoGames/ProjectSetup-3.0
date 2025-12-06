from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class LatexProject(BaseProject):
    language = ProjectType.TEX
    basestruture = {}
