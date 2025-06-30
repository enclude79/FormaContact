# Настройка окружения для Telegram бота

## Требования
- Windows 10/11
- Anaconda или Miniconda

## Шаги установки

### 1. Настройка PATH для PowerShell
```powershell
$env:PATH += ";C:\Users\$env:USERNAME\anaconda3;C:\Users\$env:USERNAME\anaconda3\Scripts;C:\Users\$env:USERNAME\anaconda3\condabin"
```

### 2. Инициализация conda для PowerShell
```powershell
conda init powershell
```

### 3. Создание виртуального окружения
```powershell
conda create -n telegram_bot python=3.11 -y
```

### 4. Активация окружения
```powershell
conda activate telegram_bot
```

### 5. Установка зависимостей
```powershell
pip install python-telegram-bot requests
```

## Запуск бота

### Вариант 1: Через PowerShell
```powershell
conda activate telegram_bot
python telegram_bot.py
```

### Вариант 2: Через bat файл
Просто запустите `start_bot.bat`

### Вариант 3: Прямой путь к Python
```powershell
C:\Users\Administrator\anaconda3\envs\telegram_bot\python.exe telegram_bot.py
```

## Структура проекта

- `telegram_bot.py` - основной файл бота
- `start_bot.bat` - скрипт для запуска бота
- `requirements.txt` - зависимости Python
- `SETUP_PYTHON.md` - эта инструкция

## Особенности бота

- **Интерактивный интерфейс** с кнопками
- **Валидация данных** (имя и телефон)
- **Форматирование номеров** телефона
- **Отправка заявок** администратору
- **Состояние диалога** для каждого пользователя

## Конфигурация

В файле `telegram_bot.py` настройте:
- `BOT_TOKEN` - токен вашего бота
- `ADMIN_CHAT_ID` - ID чата для получения заявок

## Тестирование

1. Запустите бота
2. В Telegram найдите вашего бота
3. Отправьте команду `/start`
4. Нажмите кнопку "📝 Оставить заявку"
5. Введите имя и телефон
6. Проверьте получение заявки в админ-чате 