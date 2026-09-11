from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

TClient = TypeVar("TClient")


@dataclass
class AIClient(ABC, Generic[TClient]):
    model: str = ""
    key: str = ""
    client: Optional[TClient] = None

    def configClient(self) -> bool:
        raise NotImplementedError("Feature not implemented")

    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate_with_model(self, prompt: str, model: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def list_models(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    async def list_models(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def cachead_models_list(self, models: list[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def cachead_models_list(self, models: list[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    def switch_model(self, model_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def switch_model(self, model_id: str) -> None:
        raise NotImplementedError
