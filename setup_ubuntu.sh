#!/bin/bash

# Скрипт для установки и настройки Telegram бота на Ubuntu сервере

echo "🚀 Настройка Telegram бота для анализа недвижимости 🚀"
echo "=================================================="

# Обновление системы
echo "📦 Обновление системы..."
sudo apt update && sudo apt upgrade -y

# Установка Python и pip
echo "🐍 Установка Python и необходимых пакетов..."
sudo apt install -y python3 python3-pip python3-venv git

# Создание пользователя для бота (если не существует)
if ! id "telegram_bot" &>/dev/null; then
    echo "👤 Создание пользователя telegram_bot..."
    sudo useradd -m -s /bin/bash telegram_bot
fi

# Создание директории проекта
echo "📁 Создание директории проекта..."
sudo mkdir -p /opt/telegram_bot
sudo chown telegram_bot:telegram_bot /opt/telegram_bot

# Переключение на пользователя telegram_bot для дальнейших операций
echo "🔄 Настройка проекта..."

# Создание виртуального окружения
sudo -u telegram_bot python3 -m venv /opt/telegram_bot/venv

# Копирование файлов проекта
if [ -d "/tmp/FormaContact" ]; then
    echo "📋 Копирование файлов проекта..."
    sudo cp -r /tmp/FormaContact/* /opt/telegram_bot/
    sudo chown -R telegram_bot:telegram_bot /opt/telegram_bot/
fi

# Активация виртуального окружения и установка зависимостей
echo "📦 Установка Python зависимостей..."
sudo -u telegram_bot /opt/telegram_bot/venv/bin/pip install --upgrade pip
sudo -u telegram_bot /opt/telegram_bot/venv/bin/pip install -r /opt/telegram_bot/requirements.txt

# Создание .env файла
echo "⚙️ Настройка переменных окружения..."
if [ ! -f "/opt/telegram_bot/.env" ]; then
    sudo -u telegram_bot cp /opt/telegram_bot/env.example /opt/telegram_bot/.env
    echo ""
    echo "❗ ВАЖНО: Отредактируйте файл /opt/telegram_bot/.env"
    echo "   Замените значения на реальные:"
    echo "   BOT_TOKEN=ваш_реальный_токен_бота"
    echo "   ADMIN_CHAT_ID=ваш_реальный_chat_id"
    echo ""
    echo "   Например:"
    echo "   BOT_TOKEN=7938681156:AAH2u5fCkOoLPZI9BMQxEdxdSId5xsvycaw"
    echo "   ADMIN_CHAT_ID=1717714804"
    echo ""
fi

# Создание systemd службы
echo "🔧 Создание systemd службы..."
sudo tee /etc/systemd/system/telegram-bot.service > /dev/null <<EOF
[Unit]
Description=Telegram Bot для анализа недвижимости
After=network.target

[Service]
Type=simple
User=telegram_bot
Group=telegram_bot
WorkingDirectory=/opt/telegram_bot
Environment=PATH=/opt/telegram_bot/venv/bin
ExecStart=/opt/telegram_bot/venv/bin/python /opt/telegram_bot/telegram_bot.py
Restart=always
RestartSec=10

# Ограничения безопасности
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/telegram_bot

[Install]
WantedBy=multi-user.target
EOF

# Создание скрипта для запуска
echo "📜 Создание скриптов управления..."
sudo tee /opt/telegram_bot/start.sh > /dev/null <<EOF
#!/bin/bash
# Скрипт запуска бота
source /opt/telegram_bot/venv/bin/activate
cd /opt/telegram_bot
python telegram_bot.py
EOF

sudo tee /opt/telegram_bot/stop.sh > /dev/null <<EOF
#!/bin/bash
# Скрипт остановки бота
sudo systemctl stop telegram-bot
EOF

sudo tee /opt/telegram_bot/restart.sh > /dev/null <<EOF
#!/bin/bash
# Скрипт перезапуска бота
sudo systemctl restart telegram-bot
sudo systemctl status telegram-bot
EOF

sudo tee /opt/telegram_bot/status.sh > /dev/null <<EOF
#!/bin/bash
# Проверка статуса бота
sudo systemctl status telegram-bot
EOF

sudo tee /opt/telegram_bot/logs.sh > /dev/null <<EOF
#!/bin/bash
# Просмотр логов бота
sudo journalctl -u telegram-bot -f
EOF

# Установка прав на выполнение
sudo chmod +x /opt/telegram_bot/*.sh

# Перезагрузка systemd и включение службы
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot

# Создание конфигурации для UFW (если установлен)
if command -v ufw >/dev/null 2>&1; then
    echo "🔥 Настройка брандмауэра..."
    sudo ufw allow ssh
    sudo ufw allow 22/tcp
    echo "Брандмауэр настроен для SSH доступа"
fi

echo ""
echo "✅ Установка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Отредактируйте файл: sudo nano /opt/telegram_bot/.env"
echo "   Добавьте ваши данные:"
echo "   BOT_TOKEN=your_actual_bot_token"
echo "   ADMIN_CHAT_ID=your_actual_chat_id"
echo ""
echo "2. Запустите бота: sudo systemctl start telegram-bot"
echo ""
echo "🔧 Полезные команды:"
echo "   Статус:       sudo systemctl status telegram-bot"
echo "   Запуск:       sudo systemctl start telegram-bot"
echo "   Остановка:    sudo systemctl stop telegram-bot"
echo "   Перезапуск:   sudo systemctl restart telegram-bot"
echo "   Логи:         sudo journalctl -u telegram-bot -f"
echo ""
echo "📁 Проект установлен в: /opt/telegram_bot"
echo "🎉 Готово к работе!" 