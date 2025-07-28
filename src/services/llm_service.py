from typing import Callable
from openai import OpenAI
from ..config import config

class OpenAILLMService:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)

    def stream_completion(self, document_content: str, on_token: Callable[[str], None]):
        """Chama a API do OpenAI com a nova sintaxe de cliente."""
        prompt = f"Faça uma análise crítica e detalhada em PT   -BR do seguinte documento, identificando pontos fortes, fracos e possíveis cláusulas faltantes:\n\n{document_content}"
        
        stream = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        
        for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            if token:
                on_token(token)