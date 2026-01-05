import httpx

from src.config import config
from src.services.base import BaseModelService


class GeminiService(BaseModelService):
    async def generate(self, *, text: str, user_id: int) -> str:
        pass

    async def _request(self, *, text: str, user_id: int) -> str:
        pass
