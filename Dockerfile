FROM python:3.10
WORKDIR /app
COPY requirements.txt .

# Install necessary audio libraries
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    pulseaudio \
    libasound2 \
    libasound2-dev \
    libpulse-dev \
    alsa-utils

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Set SDL to use a dummy audio driver
ENV SDL_AUDIODRIVER=dummy

CMD ["python", "juego.py"]
