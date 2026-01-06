from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class JavaProject(BaseProject):
    language = ProjectType.JAVA
    basestruture = {}
