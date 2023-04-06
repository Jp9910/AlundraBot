FROM python:3.10-slim

# Install necessary apt packages
RUN apt-get update -y && apt-get install -y vim git ffmpeg

# Set working directory
WORKDIR /app/

# Install required python extensions
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade --requirement requirements.txt

COPY ./src/ ./src/
COPY ./chaves.wav /app/

# Start bot
CMD [ "python", "/app/src/bot.py" ]