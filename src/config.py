from dataclasses import dataclass

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_GROUP_ID: str

    TOPIC_USER_MESSAGES: str
    TOPIC_MODEL_RESPONSES: str

    GEMINI_API_KEY: str
    GEMINI_MODEL: str
    GEMINI_BASE_URL: str
    GEMINI_TIMEOUT_SEC: float

    model_config = SettingsConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


@dataclass(frozen=True, slots=True)
class KafkaConsumerConfig:
    bootstrap_servers: str
    group_id: str
    auto_offset_reset: str = "earliest"
    enable_auto_commit: bool = True


@dataclass(frozen=True, slots=True)
class KafkaProducerConfig:
    bootstrap_servers: str
    linger_ms: int = 5
    acks: str = "all"


config = Config()
