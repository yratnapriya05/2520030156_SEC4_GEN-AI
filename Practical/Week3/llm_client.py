
# llm_client.py

import os
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()


class LLMClient:

    def __init__(self, provider="gemini"):
        self.provider = provider.lower()

        if self.provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")

            if not api_key:
                raise ValueError("GEMINI_API_KEY is missing in .env")

            self.client = genai.Client(api_key=api_key)
            self.model = os.getenv(
                "GEMINI_MODEL", "gemini-2.5-flash"
            )

        elif self.provider == "ollama":
            self.model = os.getenv(
                "OLLAMA_MODEL", "llama3.2"
            )
            self.url = "http://localhost:11434/api/generate"

        else:
            raise ValueError("Unsupported provider")

    def generate(self, prompt):

        if self.provider == "gemini":

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            usage = response.usage_metadata

            input_tokens = (
                usage.prompt_token_count if usage else 0
            )

            output_tokens = (
                usage.candidates_token_count if usage else 0
            )

            return {
                "provider": "GeminiProvider",
                "model": self.model,
                "response": response.text,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens
            }

        else:

            result = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )

            result.raise_for_status()
            data = result.json()

            return {
                "provider": "OllamaProvider",
                "model": self.model,
                "response": data["response"],
                "input_tokens": data.get("prompt_eval_count", 0),
                "output_tokens": data.get("eval_count", 0)
            }
