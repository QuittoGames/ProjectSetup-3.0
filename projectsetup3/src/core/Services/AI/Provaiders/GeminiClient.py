import os
from google import genai
from dotenv import load_dotenv
from dataclasses import dataclass

from core.models.AI.AIClient import AIClient

@dataclass
class GeminiClient(AIClient):
    model: str = ""
    def __init__(self):
        raise NotImplementedError("API legada: implementação do GeminiClient não está disponível.")
        # load_dotenv()

        # self.model = "gemini-2.5-flash"

        # api_key = os.getenv("GEMINI_API_KEY")
        # if not api_key:
        #     raise EnvironmentError("GEMINI_API_KEY não encontrada no .env")

        # self.client = genai.Client()

    def generete(self, promt:str) -> str:
        pass

    def listModels(self) -> list[str]:
        pass

    def switchModel(self, idModel:str) -> bool:
        pass

    def generteText(self,promt:str) -> str:
        raise NotImplementedError("API not foundd , check for new func for the genereteText for provaiders of AI")
        # response = self.client.models.generate_content(
        #     model=self.model,
        #     contents=promt
        # )

        # if not response or not response.text:
        #     raise RuntimeError("Resposta vazia do Gemini")

        # return response.text.strip()
