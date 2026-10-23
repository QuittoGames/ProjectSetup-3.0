from abc import ABC
from projectsetup3.src.core.models.Projects.Project import Project

class ProjectProtocol(ABC):
    @classmethod
    def create(name:str,
               path:str,
               language:str,
               gitRepoLink: str | None = None,
               content: str | None = None,
            ) -> None: ...

    @classmethod
    def loadProjectConfiguration(project:Project) -> Project: ...
