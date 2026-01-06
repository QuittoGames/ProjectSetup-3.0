from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class HTMLProject(BaseProject): #Need create web Project Type
    language = ProjectType.HTML
    basestruture = {}
