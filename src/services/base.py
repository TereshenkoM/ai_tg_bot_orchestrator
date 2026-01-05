from abc import ABC, abstractmethod


class BaseModelService(ABC):
    async def generate(self, *, text: str, user_id: int) -> str:
        return await self._request(text=text, user_id=user_id)

    @abstractmethod
    async def _request(self, *, text: str, user_id: int) -> str:
        raise NotImplementedError
