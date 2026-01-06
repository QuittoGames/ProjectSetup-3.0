from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class MobileProject(BaseProject):
    language = ProjectType.MOBILE
    basestruture = {}
