from projectsetup3.src.core.Services.Engine.ProjectService import ProjectService
from projectsetup3.src.core.Services.Engine.ProjectFactory import ProjectFactory
from projectsetup3.src.core.config import Config

class ProjectManager:
    _service: ProjectService | None = None
    _config: Config | None = None

    def __init__(
        config: Config,
        service: ProjectService,
    ) -> None:
        ProjectManager._config = config
        ProjectManager._service = service

    def create(self ,name:str, language:str , gitRepoLink: str | None = None , content:str | None = None) -> None:
        try:
            self._service.create_project(name=name, language=language, gitRepoLink=gitRepoLink, content=content)
        except ValueError as e:
            raise ValueError(f"ps3 | {type(e).__name__} | SDK: {e}")
        except NotADirectoryError as e:
            raise NotADirectoryError(f"ps3 | {type(e).__name__} | SDK: {e}")
        except FileNotFoundError as E:
            raise FileNotFoundError(f"ps3 | {type(e).__name__} | SDK: {e}")

    def loadProjectConfiguration(self, project: Project) -> Project:
        try:
            return self._service.loadProjectConfiguration(project=project)
        except ModuleNotFoundError as MNF:
            raise RuntimeError(f"ps3 | {type(e).__name__} | SDK: {e}")
        except FileNotFoundError as FNFE:
            raise FileNotFoundError(f"ps3 | {type(e).__name__} | SDK: {e}")

    @staticmethod
    def listSupportedLanguages() -> list[str]:
        result = ProjectService.list_supported_languages()
        return result if result is not None else []
