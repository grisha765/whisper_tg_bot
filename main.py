from faster_whisper import WhisperModel
from threading import Lock
from argparse import ArgumentParser
from telebot.async_telebot import AsyncTeleBot
from os import remove
from concurrent.futures import ThreadPoolExecutor
import uuid
import glob
import ffmpeg
import asyncio

lock = asyncio.Lock()
executor = ThreadPoolExecutor()

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

TOKEN = args.token
bot = AsyncTeleBot(TOKEN)
model_size = args.model
model = WhisperModel(model_size, device="cpu", cpu_threads=args.cpu_threads, compute_type="int8")

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


# голосовые сообщения
@bot.message_handler(content_types=['voice'])
async def voice_processing(message):
    filename = str(uuid.uuid4())
    file_name_full = "/tmp/" + filename + ".ogg"
    file_info = await bot.get_file(message.voice.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    sent_message = await bot.reply_to(message, f"Идёт расшифровка с помощью Whisper {model_size}...")
    async with lock:
        text = await recognise_async(file_name_full)
        try:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text="Текст:" + text)
        except:
            pass

    remove(file_name_full)

# видео кружки
@bot.message_handler(content_types=['video_note'])
async def video_processing(message):
    filename = str(uuid.uuid4())
    file_name_full = "/tmp/" + filename + ".mp4"
    file_info = await bot.get_file(message.video_note.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    sent_message = await bot.reply_to(message, f"Идёт расшифровка с помощью Whisper {model_size}...")
    audio_file_name_full = "/tmp/" + filename + ".wav"
    ffmpeg.input(file_name_full).output(audio_file_name_full, loglevel='quiet').run(overwrite_output=True)
    async with lock:
        text = await recognise_async(audio_file_name_full)
        try:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text="Текст:" + text)
        except:
            pass

    remove(file_name_full)
    remove(audio_file_name_full)

try:
    asyncio.run(bot.polling(none_stop=True))
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    mp4_files = glob.glob('/tmp/*.mp4')
    for filemp4_path in mp4_files:
        remove(filemp4_path)
    ogg_files = glob.glob('/tmp/*.ogg')
    for fileogg_path in ogg_files:
        remove(fileogg_path)
    wav_files = glob.glob('/tmp/*.wav')
    for filewav_path in wav_files:
        remove(filewav_path)

