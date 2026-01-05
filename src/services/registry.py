from src.services.base import BaseModelService
from src.services.gemini import GeminiService


class ModelServiceRegistry:
    def __init__(self) -> None:
        self._services: dict[str, BaseModelService] = {
            "gemini": GeminiService(),
        }

    def get(self, model: str) -> BaseModelService:
        key = model.strip().lower()
        service = self._services.get(key)

        if not service:
            raise ValueError(f"Неизвестная модель: {model}")

        return service
