# 🏠 FormaContact - Telegram Бот для Анализа Недвижимости

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-Latest-blue.svg)](https://core.telegram.org/bots/api)

Современный Telegram бот для сбора заявок клиентов на анализ недвижимости с красивым интерфейсом и валидацией данных.

## ✨ Особенности

- 🎨 **Яркий дизайн** с 300+ эмодзи
- 📱 **Валидация телефонов** - российские и международные номера
- 🌍 **Поддержка международных номеров** (Россия, Украина, США, Германия, Франция, Китай, Великобритания)
- 🔄 **Интерактивный интерфейс** с кнопками
- ⚡ **Мгновенная отправка** заявок администратору
- 🛡️ **Безопасность** - проверка и очистка данных
- 🔐 **Переменные окружения** для безопасного хранения секретов
- 🐧 **Готов к развертыванию** на Ubuntu сервере

## 🚀 Быстрый старт на локальной машине

### 1. Клонирование репозитория
```bash
git clone https://github.com/enclude79/FormaContact.git
cd FormaContact
```

### 2. Создание виртуального окружения
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
Создайте файл `.env` на основе `env.example`:
```bash
cp env.example .env
```

Отредактируйте `.env` файл:
```env
BOT_TOKEN=ваш_токен_бота
ADMIN_CHAT_ID=ваш_chat_id
```

### 5. Запуск бота
```bash
python telegram_bot.py
```

## 🐧 Развертывание на Ubuntu сервере

### Автоматическая установка (рекомендуется)

1. **Подключитесь к серверу:**
```bash
ssh enclude@89.169.166.179
```

2. **Загрузите проект:**
```bash
git clone https://github.com/enclude79/FormaContact.git /tmp/FormaContact
cd /tmp/FormaContact
```

3. **Запустите скрипт установки:**
```bash
chmod +x setup_ubuntu.sh
sudo ./setup_ubuntu.sh
```

4. **Настройте переменные окружения:**
```bash
sudo nano /opt/telegram_bot/.env
```
Добавьте ваши данные:
```env
BOT_TOKEN=ваш_реальный_токен_бота
ADMIN_CHAT_ID=ваш_реальный_chat_id
```

5. **Запустите бота:**
```bash
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

### Управление ботом на сервере

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

# Автозапуск при загрузке системы
sudo systemctl enable telegram-bot
```

### Ручная установка на Ubuntu

Если автоматический скрипт не подходит:

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python
sudo apt install -y python3 python3-pip python3-venv git

# Создание пользователя
sudo useradd -m -s /bin/bash telegram_bot

# Создание директории
sudo mkdir -p /opt/telegram_bot
sudo chown telegram_bot:telegram_bot /opt/telegram_bot

# Клонирование проекта
cd /opt/telegram_bot
sudo -u telegram_bot git clone https://github.com/enclude79/FormaContact.git .

# Виртуальное окружение
sudo -u telegram_bot python3 -m venv venv
sudo -u telegram_bot venv/bin/pip install -r requirements.txt

# Настройка .env
sudo -u telegram_bot cp env.example .env
sudo nano /opt/telegram_bot/.env  # Добавьте ваши данные
```

## 🎯 Как получить токен бота

1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте команду `/newbot`
3. Выберите имя для бота
4. Получите токен и добавьте в `.env` файл

## 📋 Как узнать Chat ID

1. Найдите [@userinfobot](https://t.me/userinfobot) в Telegram
2. Отправьте команду `/start`
3. Получите ваш User ID и добавьте в `.env` файл

## 🏗️ Структура проекта

```
FormaContact/
├── telegram_bot.py          # Основной файл бота
├── requirements.txt         # Python зависимости
├── setup_ubuntu.sh          # Скрипт установки на Ubuntu
├── start_bot.bat           # Запуск на Windows
├── .env                    # Переменные окружения (создается пользователем)
├── env.example             # Пример файла переменных
├── .gitignore              # Исключения для Git
├── README.md               # Документация
├── SETUP_PYTHON.md         # Инструкции по установке Python
└── test_bot.py             # Тесты бота
```

## 🔐 Безопасность

- **Переменные окружения**: Все секретные данные хранятся в `.env` файле
- **Git игнор**: Файл `.env` исключен из репозитория
- **Системная служба**: Бот запускается от отдельного пользователя `telegram_bot`
- **Ограничения доступа**: Настроены системные ограчения безопасности

## 🎨 Дизайн-система

### Цветовая палитра 2024-2025
- 🔥 **Cherry Red** (#FF654F) - энергия и страсть
- 💛 **Butter Yellow** (#EDEAB1) - тепло и комфорт  
- 🌊 **Aura Indigo** (#71ADBA) - доверие и профессионализм
- 🌿 **Dill Green** (#4CAE4F) - рост и стабильность
- ⭐ **Celestial Yellow** (#FFEC3D) - оптимизм и успех

### 300+ эмодзи для позитивного взаимодействия
Бот использует тщательно подобранные эмодзи для создания веселой и дружелюбной атмосферы.

## 📊 Функциональность

### Сбор данных
- ✅ Имя клиента (валидация минимум 2 символа)
- ✅ Номер телефона с автоформатированием
- ✅ Информация о пользователе Telegram

### Валидация телефонов
- 🇷🇺 **Российские номера**: точно 11 цифр, красивое форматирование
- 🌍 **Международные**: 7-15 цифр, поддержка основных стран
- 🔄 **Автоформатирование**: +7 (916) 123-45-67

### Поддерживаемые форматы
```
Российские номера:
+7 916 123 45 67
8 (916) 123-45-67  
79161234567
9161234567

Международные:
+380 67 123 45 67 (Украина)
+1 555 123 4567 (США/Канада)
+49 30 12345678 (Германия)
+33 1 42 86 83 26 (Франция)
+86 138 0013 8000 (Китай)
+44 20 7946 0958 (Великобритания)
```

## 🛠️ Разработка

### Тестирование
```bash
python test_bot.py
```

### Проверка валидации телефонов
```bash
python test_phone_validation.py
```

## 🔧 Устранение неполадок

### Конфликт экземпляров бота
Если получаете ошибку "Conflict: terminated by other getUpdates request":
```bash
# Остановите все экземпляры
sudo systemctl stop telegram-bot
pkill -f telegram_bot.py

# Подождите 30 секунд и запустите снова
sudo systemctl start telegram-bot
```

### Проверка логов
```bash
# Системные логи
sudo journalctl -u telegram-bot -f

# Если бот не запускается
sudo systemctl status telegram-bot -l
```

## 📝 Лицензия

MIT License - смотрите файл LICENSE для подробностей.

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📞 Поддержка

Если у вас есть вопросы или предложения, создайте [Issue](https://github.com/enclude79/FormaContact/issues) в этом репозитории.

---
**Сделано с ❤️ для анализа недвижимости** 