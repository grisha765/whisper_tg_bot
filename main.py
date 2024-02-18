from faster_whisper import WhisperModel
from threading import Lock
import telebot
import uuid
import os
import re
import ffmpeg
import argparse
# lock
lock = Lock()

parser = argparse.ArgumentParser(description='Telegram-бот с аргументом токена')
parser.add_argument('-t', '--token', type=str, help='Токен Telegram-бота')
args = parser.parse_args()
if not args.token:
    parser.error('Аргумент токена является обязательным. (-t TOKEN или --token TOKEN)')

TOKEN=args.token
bot = telebot.TeleBot(TOKEN)
model_size = "medium" # tiny, tiny.en, base, base.en, small, small.en, medium, medium.en, large-v1, large-v2, large-v3, or large
model = WhisperModel(model_size, device="cpu", cpu_threads=4, compute_type="int8")

def recognise(path):
    segments, info = model.transcribe(path, beam_size=5, language="ru", vad_filter=True)
    output_data = []
    for segment in segments:
        text = segment.text
        output_data.append(text)
    return "".join(output_data)

# голосовые сообщения
@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = str(uuid.uuid4())
    file_name_full="/tmp/"+filename+".ogg"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    sent_message = bot.reply_to(message, f"Идёт расшифровка с помощью Whisper {model_size}...")
    with lock:
        text=recognise(file_name_full)
        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text="Текст:" + text)
        except:
            pass

    os.remove(file_name_full)

# видео кружки
@bot.message_handler(content_types=['video_note'])
def video_processing(message):
    filename = str(uuid.uuid4())
    file_name_full = "/tmp/" + filename + ".mp4"
    file_info = bot.get_file(message.video_note.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    sent_message = bot.reply_to(message, f"Идёт расшифровка с помощью Whisper {model_size}...")
    audio_file_name_full = "/tmp/" + filename + ".wav"
    ffmpeg.input(file_name_full).output(audio_file_name_full, loglevel='quiet').run(overwrite_output=True)
    with lock:
        text = recognise(audio_file_name_full)
        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text="Текст:" + text)
        except:
            pass

    os.remove(file_name_full)
    os.remove(audio_file_name_full)

bot.polling(none_stop=True)
