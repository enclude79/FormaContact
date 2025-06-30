# 🔧 Git команды для FormaContact

Краткое руководство по размещению проекта на GitHub.

## 📋 Подготовка к коммиту

### 1. Проверка статуса
```bash
git status
```

### 2. Добавление всех файлов
```bash
git add .
```

### 3. Исключение лишних файлов (уже настроено в .gitignore)
- `.env` - переменные окружения с секретами
- `__pycache__/` - скомпилированные Python файлы
- `*.log` - файлы логов
- `node_modules/` - зависимости Node.js (удалены)

## 🚀 Первый коммит

```bash
# Инициализация репозитория (если еще не сделано)
git init

# Добавление всех файлов
git add .

# Первый коммит
git commit -m "🎉 Initial commit: Telegram bot for real estate analytics

Features:
- ✨ Bright design with 300+ emoji
- 📱 Phone validation (Russian + International)
- 🔐 Environment variables for secrets
- 🐧 Ubuntu server deployment ready
- 🐳 Docker support
- 🛡️ Security configurations"

# Добавление удаленного репозитория
git remote add origin https://github.com/enclude79/FormaContact.git

# Отправка на GitHub
git push -u origin main
```

## 📝 Последующие коммиты

```bash
# Проверка изменений
git status
git diff

# Добавление файлов
git add .

# Коммит с описанием
git commit -m "🔧 Update: описание изменений"

# Отправка на GitHub
git push
```

## 🔄 Обновление на сервере

После пуша на GitHub, обновите проект на сервере:

```bash
# Подключение к серверу
ssh enclude@89.169.166.179

# Обновление проекта
cd /opt/telegram_bot
sudo -u telegram_bot git pull origin main

# Перезапуск бота
sudo systemctl restart telegram-bot
sudo systemctl status telegram-bot
```

## 📂 Структура проекта для Git

```
FormaContact/
├── 🤖 telegram_bot.py          # Основной бот
├── 📦 requirements.txt         # Python зависимости
├── 🔧 setup_ubuntu.sh          # Установка на Ubuntu
├── 🚀 deploy_to_server.sh      # Автоматическое развертывание
├── 🐳 Dockerfile              # Docker образ
├── 🐳 docker-compose.yml      # Docker Compose
├── 📋 env.example             # Пример переменных окружения
├── 🚫 .gitignore              # Исключения Git
├── 📖 README.md               # Основная документация
├── 📖 DEPLOY.md               # Руководство по развертыванию
├── 🧪 test_bot.py             # Тесты бота
├── 🧪 test_phone_validation.py # Тесты валидации
├── 🎨 DESIGN_COLORS.md        # Цветовая палитра
├── 📝 CHANGELOG_BRIGHT_DESIGN.md # История изменений
├── 🔧 start_bot.bat           # Запуск на Windows
└── 📞 channel_*.txt           # Файлы для настройки канала
```

## ⚠️ Важные моменты

1. **НЕ коммитьте секреты**:
   - `.env` файл исключен из Git
   - Токены и ID хранятся в переменных окружения

2. **Проверяйте .gitignore**:
   - Все секретные файлы должны быть исключены
   - Временные файлы не попадают в репозиторий

3. **Осмысленные коммиты**:
   - Используйте эмодзи для типа изменений
   - Описывайте что и зачем изменили

## 🎯 Полезные алиасы

Добавьте в `~/.gitconfig`:

```ini
[alias]
    st = status
    co = checkout
    br = branch
    cm = commit -m
    lg = log --oneline --graph --all
    pushf = push --force-with-lease
```

Использование:
```bash
git st        # вместо git status
git cm "Fix"  # вместо git commit -m "Fix"
git lg        # красивый лог
``` 