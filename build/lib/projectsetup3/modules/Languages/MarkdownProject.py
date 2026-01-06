from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class MarkdownProject(BaseProject):
    language = ProjectType.MARKDOWN
    basestruture = {}
