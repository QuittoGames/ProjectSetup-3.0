from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class WebProject(BaseProject):
    language = ProjectType.WEB
    basestruture = {}
