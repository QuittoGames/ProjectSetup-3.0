from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class RobloxLuaProject(BaseProject):
    language = ProjectType.ROBLOX_LUA
    basestruture = {}
