# whisper_tg_bot

### Initial Setup

1. **Clone the repository**: Clone this repository using `git clone`.

2. **Create Virtual Env**: Create a Python Virtual Env `venv` to download the required dependencies and libraries.

3. **Download Dependencies**: Download the required dependencies into the Virtual Env `venv` using `pip`.

```shell
git clone https://github.com/grisha765/whisper_tg_bot.git
cd whisper_tg_bot
python3 -m venv venv
venv/bin/pip3 install pyTelegramBotAPI faster-whisper ffmpeg-python
```

### Run Bot

**Start an Instance**: Start an instance from the `venv` virtual environment by entering your `TOKEN` using the `-t` argument received from @BotFather and also specifying the number of threads you want to allocate using the `-cpu` argument instance, and the size of the bot model using `-m`.

```shell
venv/bin/python3 main.py -t TOKEN -cpu CPU_THREADS -m MODEL_SIZE
```
