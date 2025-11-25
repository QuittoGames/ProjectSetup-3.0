from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class LuaProject(BaseProject):
    language = ProjectType.LUA
    basestruture = {}
