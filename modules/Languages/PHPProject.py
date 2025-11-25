from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class PHPProject(BaseProject):
    language = ProjectType.PHP
    basestruture = {}
