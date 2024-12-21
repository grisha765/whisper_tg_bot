from pyrogram import Client, filters

import asyncio

from recognition.func import recognise_async
from recognition.audio import voice
from recognition.video import video_note

from config.config import Config
from config import logging_config
logging = logging_config.setup_logging(__name__)

lock = asyncio.Lock()

bot_id = []

app = Client("whisper_bot", api_id=Config.tg_id, api_hash=Config.tg_hash, bot_token=Config.tg_token)
user = Client(f"{Config.sessions_path}/whisper_user", api_id=Config.tg_id, api_hash=Config.tg_hash)

@app.on_message(filters.voice)
async def handle_audio(_, message):
    logging.debug("bot: voice message recognition...")
    await voice(message, lock, recognise_async)

@app.on_message(filters.video_note)
async def handle_video_note(_, message):
    logging.debug("bot: video note recognition...")
    await video_note(message, lock, recognise_async)

@user.on_message(filters.voice & filters.me)
async def handle_user_audio(client, message):
    if bot_id:
        async for member in client.get_chat_members(message.chat.id):
            if member.user.id == bot_id[0]:
                logging.warning(f"Bot is in the chat {message.chat.id}. Userbot will ignore this voice message.")
                return
    logging.debug("user: voice message recognition...")
    await voice(message, lock, recognise_async)

@user.on_message(filters.video_note & filters.me)
async def handle_user_video_note(client, message):
    if bot_id:
        async for member in client.get_chat_members(message.chat.id):
            if member.user.id == bot_id[0]:
                logging.warning(f"Bot is in the chat {message.chat.id}. Userbot will ignore this video note.")
                return
    logging.debug("user: video note recognition...")
    await video_note(message, lock, recognise_async)

async def start_bot():
    if Config.mode == "bot" or Config.mode == "mixed":
        logging.info("Launching the bot...")
        await app.start()
    if Config.mode == "user" or Config.mode == "mixed":
        if Config.mode == "mixed":
            bot_me = await app.get_me()
            bot_id.append(bot_me.id)
            logging.info(f"Bot ID: {bot_id[0]}")
        logging.info("Launching the user bot...")
        if Config.tg_id == "1" or Config.tg_hash == "b6b154c3707471f5339bd661645ed3d6":
            logging.error("You need to use your own TG_ID and TG_HASH value for userbot")
            import os
            os._exit(1)
        await user.start()

async def stop_bot():
    if Config.mode == "bot" or Config.mode == "mixed":
        logging.info("Stopping the bot...")
        await app.stop()
    if Config.mode == "user" or Config.mode == "mixed":
        logging.info("Stopping the user bot...")
        await user.stop()

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
