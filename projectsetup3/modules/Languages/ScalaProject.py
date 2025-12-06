from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class ScalaProject(BaseProject):
    language = ProjectType.SCALA
    basestruture = {}
