# whisper_tg_bot
Telegram bot that utilizes the Whisper model for transcription of voice messages and video notes. It is designed to run with arguments such as token, CPU threads, and model size. The bot uses Pyrogram library for interaction with Telegram, and it employs asyncio and threading for asynchronous and parallel processing.

### Initial Setup

1. **Clone the repository**: Clone this repository using `git clone`.
2. **Create Virtual Env**: Create a Python Virtual Env `venv` to download the required dependencies and libraries.
3. **Download Dependencies**: Download the required dependencies into the Virtual Env `venv` using `pip`.

```shell
git clone https://github.com/grisha765/whisper_tg_bot.git
cd whisper_tg_bot
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt 
```

### Deploy

- Run the bot:
    ```bash
    TG_TOKEN="your_telegram_bot_token" CPU_THREADS="4" MODEL_SIZE="tiny" .venv/bin/python main.py
    ```

- Other working env's:
    ```env
    LOG_LEVEL="INFO"
    TG_ID="your_telegram_api_id"
    TG_HASH="your_telegram_api_hash"
    TG_TOKEN="your_telegram_bot_token"
    CPU_THREADS="number"
    MODEL_SIZE="tiny"
    #tiny, tiny.en
    #base, base.en
    #small, small.en
    #medium, medium.en
    #large-v1, large-v2
    #large-v3, or large
    ```

### Features

1. Transcribes `voice messages` and `video notes` into text using the Whisper model.
2. Supports multiple Whisper model sizes for transcription.
3. Utilizes multithreading for efficient processing of `voice messages` and video notes.
