from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class JSONProject(BaseProject):
    language = ProjectType.JSON
    basestruture = {}
