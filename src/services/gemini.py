from src.services.base import BaseModelService
from google import genai
from src.config import config


class GeminiService(BaseModelService):
    def __init__(self) -> None:
        self._client = genai.Client()

    # TODO добавитб нормальный датакласс в ответе
    async def generate(self, *, text: str, user_id: int) -> str:
        response = self._client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=text,
        )

        return response.text

    async def _request(self, *, text: str, user_id: int) -> str:
        pass
