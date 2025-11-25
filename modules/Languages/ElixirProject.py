from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class ElixirProject(BaseProject):
    language = ProjectType.ELIXIR
    basestruture = {}
