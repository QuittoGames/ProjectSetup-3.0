from dataclasses import dataclass
import os
import json
from pathlib import Path
from projectsetup3.src.core.config.Config import Config
from projectsetup3.src.core.models.Enums.RegistredProjectType import (
    RegistredProjectType as ProjectType,
)
from projectsetup3.src.core.Services.READMEservice import READMEService
from projectsetup3.src.core.Services.History import History as HistoryService
from projectsetup3.src.core.Services.tool import tool
import datetime
import re


@dataclass
class Project:
    _language = None
    _basestruture: dict | None = None
    _name: str = ""

    def __init__(self):
        pass

    def __init__(self, name: str, basestruture: dict, language):
        self._name = (name,)
        self._basestruture = (basestruture,)
        self._language = language

    def __init__(self, name: str, basestruture: dict):
        self._name = (name,)
        self._basestruture = (basestruture,)

    def setLanguage(self, language: ProjectType):
        self.language = language

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
