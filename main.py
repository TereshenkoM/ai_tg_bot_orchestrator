import asyncio

from logger import setup_logging, get_logger

from src.runtime import OrchestratorRuntime

setup_logging(service_name="users-service")

log = get_logger(__name__)

async def main() -> None:
    runtime = OrchestratorRuntime()
    await runtime.start()
    try:
        await runtime.run()
    finally:
        await runtime.stop()


if __name__ == "__main__":
    asyncio.run(main())
