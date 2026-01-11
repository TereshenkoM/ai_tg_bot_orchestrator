import logging

from src.adapters.kafka_consumer import KafkaConsumerConfig, KafkaJsonConsumer
from src.adapters.kafka_producer import KafkaJsonProducer, KafkaProducerConfig
from src.config import config
from src.dto import ModelResponseEvent, UserMessageEvent
from src.services.registry import ModelServiceRegistry

logger = logging.getLogger(__name__)


class OrchestratorRuntime:
    def __init__(self) -> None:
        self._consumer = KafkaJsonConsumer(
            KafkaConsumerConfig(
                bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
                group_id=config.KAFKA_GROUP_ID,
                enable_auto_commit=True,
            ),
            topic=config.TOPIC_USER_MESSAGES,
        )
        self._producer = KafkaJsonProducer(
            KafkaProducerConfig(bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS)
        )
        self._registry = ModelServiceRegistry()

    async def start(self) -> None:
        await self._producer.start()
        await self._consumer.start()
        logger.info(
            f"Орекстратор запущен. topic_in={config.TOPIC_USER_MESSAGES} topic_out={config.TOPIC_MODEL_RESPONSES}",
        )

    async def stop(self) -> None:
        await self._consumer.stop()
        await self._producer.stop()
        logger.info("Оркестратор остановлен.")

    async def run(self) -> None:
        async for raw in self._consumer:
            try:
                event = UserMessageEvent.from_dict(raw)
            except Exception:
                logger.exception("Bad incoming event: %s", raw)
                continue

            try:
                service = self._registry.get(event.model)
                answer = await service.generate(text=event.text, user_id=event.user_id)
                logger.info(f'11111111 {answer}')
            except Exception as e:
                logger.error(
                    f"Ошибка при генерации модели. модель - {event.model}",
                    exc_info=e,
                )
                answer = "Не удалось получить ответ от модели. Попробуйте позже."

            out = ModelResponseEvent.build(
                user_id=event.user_id,
                chat_id=event.chat_id,
                message_id=event.message_id,
                model=event.model,
                answer=answer,
            )

            payload = out.to_dict()
            logger.info("out payload=%s", payload)

            key = str(event.user_id).encode("utf-8")
            await self._producer.send(
                config.TOPIC_MODEL_RESPONSES, out.to_dict(), key=key
            )
            await self._producer.send(
                config.TOPIC_MANAGEMENT_MESSAGES, out.to_dict(), key=key
            )