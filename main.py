import asyncio
import logging
import sys

from src.runtime import OrchestratorRuntime


async def main() -> None:
    runtime = OrchestratorRuntime()
    await runtime.start()
    try:
        await runtime.run()
    finally:
        await runtime.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
