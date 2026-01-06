from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class CSSProject(BaseProject):
    language = ProjectType.CSS
    basestruture = {}
