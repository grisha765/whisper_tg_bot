# whisper_tg_bot
Telegram bot and user bot that utilizes the Whisper model for transcription of voice messages and video notes. It is designed to run with arguments such as token, CPU threads, and model size. The bot uses Pyrogram library for interaction with Telegram, and it employs asyncio and threading for asynchronous and parallel processing.

### Initial Setup

1. **Clone the repository**: Clone this repository using `git clone`.
2. **Create Virtual Env**: Create a Python Virtual Env `venv` to download the required dependencies and libraries.
3. **Download Dependencies**: Download the required dependencies into the Virtual Env `venv` using `pip`.

```shell
git clone https://github.com/grisha765/whisper_tg_bot.git
cd whisper_tg_bot
python -m venv .venv
.venv/bin/python -m pip install uv
.venv/bin/python -m uv sync
```

### Deploy

- Run the bot:
    ```bash
    TG_TOKEN="your_telegram_bot_token" CPU_THREADS="4" MODEL_SIZE="tiny" uv run main.py
    ```

- Other working env's:
    ```env
    LOG_LEVEL="INFO"
    MODE="bot" #bot, user, mixed
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

#### Container

- Pull container:
    ```bash
    podman pull ghcr.io/grisha765/whisper_tg_bot:latest
    ```

- Deploy in container as bot:
    ```bash
    mkdir -p $HOME/whisper_cache/ && \
    podman run --tmpfs /tmp \
    --name whisper_tg_bot \
    -v $HOME/whisper_cache/:/root/.cache/huggingface/:z \
    -e MODE="bot" \
    -e TG_TOKEN="your_telegram_bot_token" \
    -e MODEL_SIZE="tiny" \
    -e CPU_THREADS="4" \
    ghcr.io/grisha765/whisper_tg_bot:latest
    ```

- Deploy in container as user bot:
    ```bash
    mkdir -p $HOME/whisper_cache/ && \
    mkdir -p $HOME/sessions/ && \
    podman run --tmpfs /tmp \
    --name whisper_tg_bot \
    -v $HOME/whisper_cache/:/root/.cache/huggingface/:z \
    -v $HOME/sessions/:/app/sessions/:z \
    -e MODE="user" \
    -e TG_ID="your_telegram_api_id" \
    -e TG_HASH="your_telegram_api_hash" \
    -e MODEL_SIZE="tiny" \
    -e CPU_THREADS="4" \
    ghcr.io/grisha765/whisper_tg_bot:latest
    ```
*use MODE="mixed" to combine modes*

### Features

1. Transcribes `voice messages` and `video notes` into text using the Whisper model.
2. Supports multiple Whisper model sizes for transcription.
3. Utilizes multithreading for efficient processing of `voice messages` and video notes.
4. Selection of the bot operating `mode`, as a `user` bot or as a `regular` bot, as well as `mixed` mode.
