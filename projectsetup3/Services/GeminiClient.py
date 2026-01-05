import os
from google import genai
from dotenv import load_dotenv

class GeminiClient:
    def __init__(self):
        load_dotenv() 
        
        self.model = "gemini-2.5-flash"

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY não encontrada no .env")
        
        self.client = genai.Client()

    def generteText(self,promt:str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=promt
        )

        if not response or not response.text:
            raise RuntimeError("Resposta vazia do Gemini")
        
        return response.text.strip()