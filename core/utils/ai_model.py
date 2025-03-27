from openai import OpenAI


class AIModel:
    def __init__(self, name: str, provider: str, base_url: str, api_key: str):
        self.name = name  # llama-3.1-8b-instant
        self.provider = provider  # groq
        self.base_url = base_url  # https://api.groq.com/openai/v1
        self.api_key = api_key

    def client(self):
        return OpenAI(api_key=self.api_key, base_url=self.base_url)
