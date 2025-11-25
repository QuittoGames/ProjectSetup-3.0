from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class RProject(BaseProject):
    language = ProjectType.R
    basestruture = {}
