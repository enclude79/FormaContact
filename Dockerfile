# Используем официальный образ Python
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя для безопасности
RUN useradd -m -u 1000 telegram_bot

# Установка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY telegram_bot.py .

# Изменение владельца файлов
RUN chown -R telegram_bot:telegram_bot /app

# Переключение на пользователя telegram_bot
USER telegram_bot

# Переменные окружения
ENV PYTHONUNBUFFERED=1

# Команда запуска
CMD ["python", "telegram_bot.py"] 