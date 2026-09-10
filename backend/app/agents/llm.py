from typing import TypeVar, Type
from pydantic import BaseModel
from openai import OpenAI
from app.config import settings

T = TypeVar("T", bound=BaseModel)

class LLMClient:
    def __init__(self):
        self.client = None if settings.mock_llm or not settings.openai_api_key else OpenAI(api_key=settings.openai_api_key)

    def structured(self, system: str, user: str, schema: Type[T], mock: T) -> T:
        if not self.client:
            return mock
        response = self.client.responses.parse(
            model=settings.openai_model,
            input=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            text_format=schema,
        )
        parsed = getattr(response, "output_parsed", None)
        if parsed is None:
            raise RuntimeError("LLM returned no structured output")
        return parsed

llm = LLMClient()
