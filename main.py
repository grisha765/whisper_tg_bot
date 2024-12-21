import asyncio, signal
from config.config import Config
from config import logging_config
logging = logging_config.setup_logging(__name__)

logging.info(f"Script initialization, logging level: {Config.log_level}")

async def main():
    from core.tg import start_bot, stop_bot
    await start_bot()

    loop = asyncio.get_running_loop()

    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGINT, stop.set_result, None)
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    try:
        await stop
    finally:
        await stop_bot()


if __name__ == '__main__':
    asyncio.run(main())
