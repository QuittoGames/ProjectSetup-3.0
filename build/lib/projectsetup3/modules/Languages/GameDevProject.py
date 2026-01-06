from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class GameDevProject(BaseProject):
    language = ProjectType.GAME_DEV
    basestruture = {}
