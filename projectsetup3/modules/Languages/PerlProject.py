from dataclasses import dataclass
from ..Interfaces.BaseProject import BaseProject
from ..Enums.ProjectType import ProjectType

@dataclass
class PerlProject(BaseProject):
    language = ProjectType.PERL
    basestruture = {}
