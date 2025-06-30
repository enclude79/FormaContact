# 🚀 Руководство по развертыванию FormaContact

Данное руководство описывает различные способы развертывания Telegram бота на продуктивном Ubuntu сервере.

## 🎯 Сервер для развертывания

- **IP адрес**: 89.169.166.179
- **Пользователь**: enclude
- **ОС**: Ubuntu
- **SSH доступ**: `ssh enclude@89.169.166.179`

## 🛠️ Метод 1: Автоматическая установка (Рекомендуется)

### Шаг 1: Подключение к серверу
```bash
ssh enclude@89.169.166.179
```

### Шаг 2: Загрузка проекта
```bash
git clone https://github.com/enclude79/FormaContact.git /tmp/FormaContact
cd /tmp/FormaContact
```

### Шаг 3: Запуск установочного скрипта
```bash
chmod +x setup_ubuntu.sh
sudo ./setup_ubuntu.sh
```

### Шаг 4: Настройка переменных окружения
```bash
sudo nano /opt/telegram_bot/.env
```

Добавьте ваши реальные данные:
```env
BOT_TOKEN=7938681156:AAH2u5fCkOoLPZI9BMQxEdxdSId5xsvycaw
ADMIN_CHAT_ID=1717714804
```

### Шаг 5: Запуск и проверка
```bash
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
sudo systemctl enable telegram-bot  # Автозапуск
```

### Проверка логов
```bash
sudo journalctl -u telegram-bot -f
```

## 🐳 Метод 2: Docker развертывание

### Предварительные требования
```bash
# Установка Docker
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

### Развертывание с Docker
```bash
# Клонирование репозитория
git clone https://github.com/enclude79/FormaContact.git
cd FormaContact

# Создание .env файла
cp env.example .env
nano .env  # Добавьте ваши данные

# Запуск через Docker Compose
docker-compose up -d

# Проверка статуса
docker-compose ps
docker-compose logs -f telegram-bot
```

### Управление Docker контейнером
```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Просмотр логов
docker-compose logs -f telegram-bot

# Обновление
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🔧 Метод 3: Ручная установка

### Шаг 1: Подготовка системы
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git
```

### Шаг 2: Создание пользователя
```bash
sudo useradd -m -s /bin/bash telegram_bot
sudo mkdir -p /opt/telegram_bot
sudo chown telegram_bot:telegram_bot /opt/telegram_bot
```

### Шаг 3: Установка проекта
```bash
cd /opt/telegram_bot
sudo -u telegram_bot git clone https://github.com/enclude79/FormaContact.git .
sudo -u telegram_bot python3 -m venv venv
sudo -u telegram_bot venv/bin/pip install -r requirements.txt
```

### Шаг 4: Настройка окружения
```bash
sudo -u telegram_bot cp env.example .env
sudo nano /opt/telegram_bot/.env
```

### Шаг 5: Создание службы systemd
```bash
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
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/telegram_bot

[Install]
WantedBy=multi-user.target
EOF
```

### Шаг 6: Запуск службы
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

## 🔍 Мониторинг и управление

### Команды управления службой
```bash
# Проверка статуса
sudo systemctl status telegram-bot

# Запуск
sudo systemctl start telegram-bot

# Остановка
sudo systemctl stop telegram-bot

# Перезапуск
sudo systemctl restart telegram-bot

# Просмотр логов
sudo journalctl -u telegram-bot -f

# Последние 100 строк логов
sudo journalctl -u telegram-bot -n 100
```

### Мониторинг производительности
```bash
# Использование ресурсов
htop
sudo systemctl status telegram-bot

# Проверка сетевых соединений
sudo netstat -tlnp | grep python

# Проверка процессов
ps aux | grep telegram_bot
```

## 🛡️ Безопасность

### Настройка брандмауэра (UFW)
```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 22/tcp
sudo ufw status
```

### Обновление системы
```bash
sudo apt update && sudo apt upgrade -y
sudo systemctl restart telegram-bot
```

### Бэкап конфигурации
```bash
# Создание архива
sudo tar -czf telegram-bot-backup-$(date +%Y%m%d).tar.gz /opt/telegram_bot

# Копирование на локальную машину
scp enclude@89.169.166.179:~/telegram-bot-backup-*.tar.gz ./
```

## 🔧 Устранение неполадок

### Проблема: Конфликт экземпляров бота
```bash
# Остановка всех экземпляров
sudo systemctl stop telegram-bot
sudo pkill -f telegram_bot.py

# Ожидание 30 секунд
sleep 30

# Запуск
sudo systemctl start telegram-bot
```

### Проблема: Бот не отвечает
```bash
# Проверка логов
sudo journalctl -u telegram-bot -f

# Проверка сетевого соединения
curl -s https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

### Проблема: Ошибки в логах
```bash
# Детальные логи
sudo journalctl -u telegram-bot -f --no-pager

# Проверка файла .env
sudo cat /opt/telegram_bot/.env

# Проверка прав доступа
ls -la /opt/telegram_bot/
```

## 📈 Обновление проекта

### Обновление из Git
```bash
cd /opt/telegram_bot
sudo -u telegram_bot git pull origin main
sudo systemctl restart telegram-bot
```

### Обновление зависимостей
```bash
cd /opt/telegram_bot
sudo -u telegram_bot venv/bin/pip install -r requirements.txt --upgrade
sudo systemctl restart telegram-bot
```

## 📞 Контакты и поддержка

При возникновении проблем:
1. Проверьте логи: `sudo journalctl -u telegram-bot -f`
2. Создайте [Issue](https://github.com/enclude79/FormaContact/issues) в репозитории
3. Опишите проблему подробно с приложением логов

## Новые файлы после развертывания

### Рабочие файлы
- `telegram_bot_current.py` - Актуальная рабочая версия бота с улучшенным логированием
- `get_admin_id.py` - Утилита для получения ID администратора
- `get_chat_id.py` - Утилита для получения Chat ID пользователей

### Системные файлы
- `formacontact-bot.service` - Systemd сервис для автозапуска бота на Ubuntu
- `env.example` - Обновленный шаблон конфигурации

### Настройка окружения
1. Скопируйте `env.example` в `.env`
2. Заполните реальными значениями:
   - `BOT_TOKEN` - токен вашего Telegram бота
   - `ADMIN_CHAT_ID` - ID чата администратора для получения заявок

### Запуск на сервере
```bash
# Установка сервиса
sudo cp formacontact-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable formacontact-bot
sudo systemctl start formacontact-bot
```

### Проверка статуса
```bash
sudo systemctl status formacontact-bot
```

## Архитектура

---
**Успешного развертывания! 🚀** 