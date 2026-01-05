from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class UserMessageEvent:
    user_id: int
    chat_id: int
    message_id: int
    text: str
    model: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "UserMessageEvent":
        return UserMessageEvent(
            user_id=int(data["user_id"]),
            chat_id=int(data["chat_id"]),
            message_id=int(data["message_id"]),
            text=str(data["text"]),
            model=str(data["model"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ModelResponseEvent:
    user_id: int
    chat_id: int
    message_id: int
    model: str
    answer: str
    created_at: str

    @staticmethod
    def build(
        *, user_id: int, chat_id: int, message_id: int, model: str, answer: str
    ) -> "ModelResponseEvent":
        return ModelResponseEvent(
            user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            model=model,
            answer=answer,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
