from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class RubyProject(BaseProject):
    language = ProjectType.RUBY
    basestruture = {}
