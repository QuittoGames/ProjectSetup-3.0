from projectsetup3.src.core.Services.Engine.ProjectService import ProjectService


class ProjectManager(ProjectService):
    def __init__(self, factory = None):
        super().__init__(factory)
