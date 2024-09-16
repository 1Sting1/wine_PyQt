# Используем базовый образ Python
FROM python:3.12-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    gnupg \
    lsb-release \
    libgtk-3-dev \
    libwebkit2gtk-4.0-dev \
    python3-rpi.gpio \
    python3-smbus \
    python3-spidev \
    i2c-tools \
    chromium \
    x11-apps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Добавление скрипта для повторных попыток установки зависимостей
RUN echo '#!/bin/sh\n\
n=0\n\
until [ "$n" -ge 5 ]\n\
do\n\
   pip install --no-cache-dir -r requirements.txt && break\n\
   n=$((n+1))\n\
   sleep 5\n\
done' > install_requirements.sh \
    && chmod +x install_requirements.sh \
    && ./install_requirements.sh

# Копируем остальные файлы проекта
COPY . .
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

RUN pip install spidev RPi.GPIO smbus

# Указываем команду для запуска приложения
CMD ["/bin/bash", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000"]
#& sleep 5 && chromium --no-sandbox --kiosk http://localhost:8000