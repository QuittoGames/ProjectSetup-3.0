from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class PowerShellProject(BaseProject):
    language = ProjectType.POWERSHELL
    basestruture = {}
