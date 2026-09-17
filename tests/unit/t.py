# Huguiinface

import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="fal-ai",
    api_key=os.environ["HF_TOKEN"],
)

# audio is returned as bytes
audio = client.text_to_speech(
    "Oi Quitto , O OpenRouter tem uma variante explicitamente :free, com preço zero para entrada e saída, embora com rate limits de modelo gratuito. Na NVIDIA, o modelo está disponível no catálogo como endpoint de trial; a documentação também mostra o ID z-ai/glm-5.3-flash.",
    model="hexgrad/Kokoro-82M",
)
