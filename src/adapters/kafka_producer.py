import json
from typing import Any

from aiokafka import AIOKafkaProducer

from src.config import KafkaProducerConfig


class KafkaJsonProducer:
    def __init__(self, cfg: KafkaProducerConfig) -> None:
        self._cfg = cfg
        self._producer: AIOKafkaProducer | None = None

    async def start(self) -> None:
        if self._producer is not None:
            return
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self._cfg.bootstrap_servers,
            linger_ms=self._cfg.linger_ms,
            acks=self._cfg.acks,
        )
        await self._producer.start()

    async def stop(self) -> None:
        if self._producer is None:
            return
        await self._producer.stop()
        self._producer = None

    async def send(
        self, topic: str, payload: dict[str, Any], *, key: bytes | None = None
    ) -> None:
        if self._producer is None:
            raise RuntimeError("producer не запущен")
        value = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        await self._producer.send_and_wait(topic, value=value, key=key)
