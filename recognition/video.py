import tempfile, ffmpeg
from config.config import Config
from config import logging_config
logging = logging_config.setup_logging(__name__)

async def video_note(message, lock, recognise_async):
    if message.video_note:
        print_message = await message.reply(f"Text recognition is in progress using: Whisper {Config.model_size}...")
        async with lock:
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=True) as temp_file_mp4:
                await message.download(file_name=temp_file_mp4.name)
                with tempfile.NamedTemporaryFile(suffix=".ogg", delete=True) as temp_file_ogg:
                    ffmpeg.input(temp_file_mp4.name).output(temp_file_ogg.name, loglevel='quiet').run(overwrite_output=True, capture_stderr=True)
                    try:
                        await print_message.edit_text(f"Text:{await recognise_async(temp_file_ogg.name)}")
                    except:
                        await print_message.edit_text(f"Whisper {Config.model_size}: Text recognition is not successful.")
                        logging.warning(f"Whisper {Config.model_size}: Text recognition is not successful.")
                temp_file_ogg.close()
            temp_file_mp4.close()

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
