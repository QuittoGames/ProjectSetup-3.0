from dataclasses import dataclass
from pathlib import Path
from projectsetup3.src.core.models.Enums.RegistredProjectType import (
    RegistredProjectType as ProjectType,
)


@dataclass
class Project:
    _language: ProjectType | None = None
    _basestruture: dict | None = None
    _name: str = ""

    def __init__(
        self,
        name: str = "",
        basestruture: dict | None = None,
        language: ProjectType | None = None,
    ):
        self._name = name
        self._basestruture = basestruture
        self._language = language

    def setLanguage(self, language: ProjectType):
        self._language = language

    def getLanguage(self) -> ProjectType | None:
        return self._language

    def setBasestruture(self, basestruture: dict):
        self._basestruture = basestruture

    def getBasestruture(self) -> dict | None:
        return self._basestruture

    def setName(self, name: str):
        self._name = name

    def getName(self) -> str:
        return self._name
