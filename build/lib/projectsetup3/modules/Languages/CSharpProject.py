from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class CSharpProject(BaseProject):
    language = ProjectType.CSHARP
    basestruture = {}
