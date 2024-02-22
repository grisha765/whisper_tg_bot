# whisper_tg_bot

### Initial Setup

1. **Clone the repository**: Clone this repository using `git clone`.

2. **Create Virtual Env**: Create a Python Virtual Env to download the required dependencies and libraries.

3. **Download Dependencies**: Download the required dependencies into the Virtual Env using `pip`.

```shell
git clone https://github.com/grisha765/whisper_tg_bot.git
cd whisper_tg_bot
python -m venv venv
venv/bin/pip install pyTelegramBotAPI faster-whisper ffmpeg-python
```

### Run Bot

**Start Instance**: Start the instance from Virtualenv by entering your `TOKEN` received in @BotFather.

```shell
venv/bin/python main.py -t TOKEN
```
