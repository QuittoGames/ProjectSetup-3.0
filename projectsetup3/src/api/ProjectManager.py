from projectsetup3.src.core.Services.Engine.ProjectService import ProjectService


class ProjectManager(ProjectService):
    """SDK público do ProjectSetup 3.0.

    Fachada de alto nível para criação de projetos. Não depende de
    TUI, CLI ou camada de aplicação.
    """
