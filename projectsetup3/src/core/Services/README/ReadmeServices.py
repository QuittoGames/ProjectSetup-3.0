from dataclasses import dataclass
from projectsetup3.src.core.config.Config import Config


@dataclass
class ReadmeService:
    config: Config = None

    def __init__(self, config: Config):
        self.config = config

    def isActive(self):
        if Config.READMEAvaliable and content and file == "README.md":
            code = READMEService.genereteREADME(
                content,
                name,
                project.getLanguage().value,
                project.getBasestruture(),
            )
