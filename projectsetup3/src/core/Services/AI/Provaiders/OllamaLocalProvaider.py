from dataclasses import dataclass
from core.models.AI.AIClient import AIClient
from ollama import Client

@dataclass
class OllamaLocalProvaider(AIClient[Client]):
    client:Client = Client

    _HOST:str = "http://localhost:11434"

    def configClient(self) -> bool:
        try:
            self.client = Client(self._HOST)
            self.client.list()
        except Exception:
            raise Exception

    def generete(self, promt:str) -> str:
        if not promt:
            raise RuntimeError("Protm is null or emptiy")

        response = self.client.chat(
            model=self.model,
            messages=[
                {"role": "user", "content": promt}
            ]
        )

    def generete(self, promt:str) -> str:
        raise NotImplementedError("Feture not impl")

    def listModels(self) -> list[str]:
        raise NotImplementedError("Feture not impl")

    def switchModel(self, idModel:str) -> bool:
        raise NotImplementedError
