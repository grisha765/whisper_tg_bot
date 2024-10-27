from faster_whisper import WhisperModel
from concurrent.futures import ThreadPoolExecutor
from pyrogram import Client, filters
import ffmpeg
import asyncio
import tempfile
from config.config import Config
from config import logging_config
logging = logging_config.setup_logging(__name__)

executor = ThreadPoolExecutor()
lock = asyncio.Lock()

app = Client("bot", api_id=Config.tg_id, api_hash=Config.tg_hash, bot_token=Config.tg_token)

model_size = Config.model_size
model = WhisperModel(model_size, device="cpu", cpu_threads=int(Config.cpu_threads), compute_type="int8")

def recognise_sync(path):
    segments, info = model.transcribe(path, beam_size=5, vad_filter=True)
    output_data = []
    for segment in segments:
        text = segment.text
        output_data.append(text)
    return "".join(output_data)

async def recognise_async(path):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, recognise_sync, path)

@app.on_message(filters.voice)
async def voice(_, message):
    if message.voice:
        print_message = await message.reply(f"Text recognition is in progress using: Whisper {model_size}...")
        async with lock:
            with tempfile.NamedTemporaryFile(delete=True) as temp_file:
                await message.download(file_name=temp_file.name)
                await print_message.edit_text(f"Text:{await recognise_async(temp_file.name)}")
            temp_file.close()

@app.on_message(filters.video_note)
async def video_note(_, message):
    if message.video_note:
        print_message = await message.reply(f"Text recognition is in progress using: Whisper {model_size}...")
        async with lock:
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=True) as temp_file_mp4:
                await message.download(file_name=temp_file_mp4.name)
                with tempfile.NamedTemporaryFile(suffix=".ogg", delete=True) as temp_file_ogg:
                    ffmpeg.input(temp_file_mp4.name).output(temp_file_ogg.name, loglevel='quiet').run(overwrite_output=True, capture_stderr=True)
                    await print_message.edit_text(f"Text:{await recognise_async(temp_file_ogg.name)}")
                temp_file_ogg.close()
            temp_file_mp4.close()

async def start_bot():
    logging.info("Launching the bot...")
    await app.start()

async def stop_bot():
    logging.info("Stopping the bot...")
    await app.stop()

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
