from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class DartProject(BaseProject):
    language = ProjectType.DART
    basestruture = {}
