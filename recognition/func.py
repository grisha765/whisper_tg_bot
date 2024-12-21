import asyncio
from faster_whisper import WhisperModel
from config.config import Config
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor()

model = WhisperModel(Config.model_size, device="cpu", cpu_threads=int(Config.cpu_threads), compute_type="int8")

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

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
