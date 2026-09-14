from dataclasses import dataclass
from pathlib import Path
from projectsetup3.src.core.models.AI.AIClient import AIClient
from projectsetup3.src.core.config.Config import Config
from ollama import AsyncClient
import asyncio
import aiofiles
import os


@dataclass
class OllamaLocalProvaider(AIClient[AsyncClient]):
    client: AsyncClient = AsyncClient

    _HOST: str = "http://localhost:11434"
    _LOG_PATH: Path = Config.appdata / ".cache" / "data.cache"

    async def configClient(self) -> bool:
        try:
            self.client = AsyncClient(host=self._HOST)
            self.client.list()

            models: list[str] = await self.list_models()
            asyncio.create_task(self.cachead_models_list(models=models))
            return True
        except ConnectionError as error:
            raise RuntimeError(
                f"Unable to connect to Ollama server at '{self._HOST}'"
            ) from error

        except TimeoutError as error:
            raise RuntimeError(
                f"Connection to Ollama server timed out at '{self._HOST}'"
            ) from error

        except OSError as error:
            raise RuntimeError(
                f"Failed to access local resources required by Ollama provider: {error}"
            ) from error

        except RuntimeError as error:
            raise RuntimeError(
                f"Failed to initialize Ollama local provider: {error}"
            ) from error

        except Exception as error:
            raise RuntimeError(
                "Unexpected error while configuring Ollama local provider"
            ) from error

    def generete(self, promt: str) -> str:
        if not promt:
            raise RuntimeError("Protm is null or emptiy")

        if not self.model:
            raise RuntimeError("model is null or emptiy")

        response = self.client.chat(
            model=self.model, messages=[{"role": "user", "content": promt}]
        )

    def list_models(self) -> list[str]:
        raise NotImplementedError

    async def listModels(self) -> list[str]:
        response = await self.client.list()

        if not response:
            raise RuntimeError("Ollama returned an empty response")

        models: list[str] = [model.model for model in response.models]

        if not self._LOG_PATH.exists():
            asyncio.create_task(self.cachead_models_list())

        return models

    async def cachead_models_list(self, models: list[str]) -> None:
        try:
            if models is None:
                raise ValueError("The models list cannot be None")

            if not isinstance(models, list):
                raise TypeError("models must be a list of strings")

            if not all(isinstance(model, str) for model in models):
                raise TypeError("models must contain only strings")

            await self._LOG_PATH.mkdir(parents=True, exist_ok=True)

            async with aiofiles.open(self._LOG_PATH, "w", encoding="utf-8") as file:
                await file.write("\n".join(i for i in models if i))

        except (OSError, TypeError, ValueError) as error:
            raise RuntimeError("Unable to cache the Ollama models list") from error

    async def switchModel(self, idModel: str) -> None:
        models: list[str] = []

        with open(self._LOG_PATH, "r", encoding="utf-8") as file:
            models = list(i.strip() for i in file if i.strip())

        if idModel not in models or idModel not in await self.listModels():
            raise RuntimeError(
                f"Model '{idModel}' is not available in the Ollama model cache"
            )

        self.model = idModel
