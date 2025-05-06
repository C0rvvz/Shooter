# Imagen base con Python
FROM python:3.11-slim

# 1. Instalar todas las dependencias del sistema en un solo RUN (mejor práctica Docker)
RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libportmidi0 \
    libfreetype6 \
    libsmpeg0 \
    libjpeg-dev \
    libtiff5-dev \
    libwebp-dev \
    libopenjp2-7-dev \
    libx11-dev \
    libxext-dev \
    libasound2-plugins \
    pulseaudio \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Directorio de trabajo y dependencias de Python
WORKDIR /Shooter

# 3. Copiar requirements.txt primero (para aprovechar caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el resto de la aplicación
COPY . .

# 5. Comando de inicio (con fallback silencioso si falla el audio)
CMD ["python", "juego.py"]