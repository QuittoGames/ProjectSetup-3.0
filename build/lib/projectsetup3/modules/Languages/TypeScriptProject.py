from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class TypeScriptProject(BaseProject):
    language = ProjectType.TYPESCRIPT
    basestruture = {}
