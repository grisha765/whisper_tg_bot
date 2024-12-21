FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

ENV SESSIONS_PATH=/app/sessions

CMD ["python", "main.py"]
