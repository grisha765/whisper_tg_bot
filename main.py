from faster_whisper import WhisperModel
from threading import Lock
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from pyrogram import Client, filters
import subprocess
import uuid
import glob
import ffmpeg
import asyncio
import tempfile

executor = ThreadPoolExecutor()
lock = asyncio.Lock()

parser = ArgumentParser(description='Telegram-бот с аргументом токена и потоками процессора.')
parser.add_argument('-t', '--token', type=str, help='Токен Telegram-бота')
parser.add_argument('-cpu', '--cpu_threads', type=int, help='Потоки процессора')
parser.add_argument('-m', '--model', type=str, help='Модель расспознователя (tiny, tiny.en, base, base.en, small, small.en, medium, medium.en, large-v1, large-v2, large-v3, or large).')
args = parser.parse_args()
if not args.token:
    parser.error('Аргумент токена является обязательным. (-t TOKEN или --token TOKEN), --help для дополнительной информации.')
if not args.model:
    parser.error('Аргумент размера модели является обязательным. (-m MODEL_SIZE или --model MODEL_SIZE), --help для дополнительной информации.')
if not args.cpu_threads or args.cpu_threads <= 0:
    parser.error("Неправильный формат для аргумента -cpu, ожидается положительное число, --help для дополнительной информации.")

api_id = 1
api_hash = 'b6b154c3707471f5339bd661645ed3d6'
bot_token = args.token
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

model_size = args.model
model = WhisperModel(model_size, device="cpu", cpu_threads=args.cpu_threads, compute_type="int8")

def get_last_commit_hash():
    try:
        result = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE)
        commit_hash = result.stdout.decode('utf-8').strip()
        return commit_hash
    except Exception as e:
        print(f"Error: {e}")
        return None
commit_hash = get_last_commit_hash()

def recognise_sync(path):
    segments, info = model.transcribe(path, beam_size=5, language="ru", vad_filter=True)
    output_data = []
    for segment in segments:
        text = segment.text
        output_data.append(text)
    return "".join(output_data)

async def recognise_async(path):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, recognise_sync, path)

@app.on_message(filters.command("help"))
async def help_command(client, message):
    help_message = await message.reply(f"Whisper Telegram Bot {commit_hash}")
    await asyncio.sleep(5)
    await help_message.delete()

# голосовые сообщения
@app.on_message(filters.voice)
async def voice(client, message):
    if message.voice:
        print_message = await message.reply(f"Идёт расшифровка с помощью Whisper {model_size}...")
        async with lock:
            with tempfile.NamedTemporaryFile(delete=True) as temp_file:
                await message.download(file_name=temp_file.name)
                await print_message.edit_text(f"Текст:{await recognise_async(temp_file.name)}")
            temp_file.close()

# видео кружки
@app.on_message(filters.video_note)
async def video_note(client, message):
    if message.video_note:
        print_message = await message.reply(f"Идёт расшифровка с помощью Whisper {model_size}...")
        async with lock:
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=True) as temp_file_mp4:
                await message.download(file_name=temp_file_mp4.name)
                with tempfile.NamedTemporaryFile(suffix=".ogg", delete=True) as temp_file_ogg:
                    ffmpeg.input(temp_file_mp4.name).output(temp_file_ogg.name, loglevel='quiet').run(overwrite_output=True, capture_stderr=True)
                    await print_message.edit_text(f"Текст:{await recognise_async(temp_file_ogg.name)}")
                temp_file_ogg.close()
            temp_file_mp4.close()
app.run()
