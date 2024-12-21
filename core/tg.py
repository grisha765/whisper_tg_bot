from pyrogram import Client, filters

import asyncio

from recognition.func import recognise_async
from recognition.audio import voice
from recognition.video import video_note

from config.config import Config
from config import logging_config
logging = logging_config.setup_logging(__name__)

lock = asyncio.Lock()

app = Client("bot", api_id=Config.tg_id, api_hash=Config.tg_hash, bot_token=Config.tg_token)

@app.on_message(filters.voice)
async def handle_audio(_, message):
    await voice(message, lock, recognise_async)

@app.on_message(filters.video_note)
async def handle_video_note(_, message):
    await video_note(message, lock, recognise_async)

async def start_bot():
    logging.info("Launching the bot...")
    await app.start()

async def stop_bot():
    logging.info("Stopping the bot...")
    await app.stop()

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
