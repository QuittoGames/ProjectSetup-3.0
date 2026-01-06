from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class AssemblyProject(BaseProject):
    language = ProjectType.ASSEMBLY
    basestruture = {}
