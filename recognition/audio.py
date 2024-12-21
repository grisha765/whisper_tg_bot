import tempfile
from config.config import Config
from config import logging_config
logging = logging_config.setup_logging(__name__)

async def voice(message, lock, recognise_async):
    if message.voice:
        print_message = await message.reply(f"Whisper {Config.model_size}: Text recognition is in progress...")
        async with lock:
            with tempfile.NamedTemporaryFile(delete=True) as temp_file:
                await message.download(file_name=temp_file.name)
                try:
                    await print_message.edit_text(f"Text:{await recognise_async(temp_file.name)}")
                except:
                    await print_message.edit_text(f"Whisper {Config.model_size}: Text recognition is not successful.")
                    logging.warning(f"Whisper {Config.model_size}: Text recognition is not successful.")
            temp_file.close()

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
