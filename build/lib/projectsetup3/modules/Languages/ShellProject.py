from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class ShellProject(BaseProject):
    language = ProjectType.SHELL
    basestruture = {}
