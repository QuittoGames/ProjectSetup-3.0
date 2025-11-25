from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class ZigProject(BaseProject):
    language = ProjectType.ZIG
    basestruture = {}
