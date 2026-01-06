from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class JavaScriptProject(BaseProject):
    language = ProjectType.JAVASCRIPT
    basestruture = {}
