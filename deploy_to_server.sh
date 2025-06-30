#!/bin/bash

# Скрипт для автоматического развертывания на Ubuntu сервер

SERVER_USER="enclude"
SERVER_IP="89.169.166.179"
REPO_URL="https://github.com/enclude79/FormaContact.git"

echo "🚀 Развертывание FormaContact на сервер Ubuntu 🚀"
echo "================================================="
echo "Сервер: $SERVER_USER@$SERVER_IP"
echo "Репозиторий: $REPO_URL"
echo ""

# Функция для выполнения команд на сервере
run_remote() {
    echo "🔧 Выполнение на сервере: $1"
    ssh $SERVER_USER@$SERVER_IP "$1"
}

# Проверка подключения к серверу
echo "📡 Проверка подключения к серверу..."
if ! ssh -o ConnectTimeout=10 $SERVER_USER@$SERVER_IP "echo 'Подключение успешно'"; then
    echo "❌ Ошибка подключения к серверу $SERVER_IP"
    echo "   Проверьте:"
    echo "   - Доступность сервера"
    echo "   - SSH ключи"
    echo "   - Сетевое соединение"
    exit 1
fi

echo ""
echo "✅ Подключение к серверу установлено"
echo ""

# Остановка существующей службы (если есть)
echo "🛑 Остановка существующей службы..."
run_remote "sudo systemctl stop telegram-bot 2>/dev/null || true"

# Удаление старой версии
echo "🗑️ Очистка старой версии..."
run_remote "rm -rf /tmp/FormaContact"

# Загрузка проекта
echo "📥 Загрузка проекта с GitHub..."
run_remote "git clone $REPO_URL /tmp/FormaContact"

# Переход в директорию и запуск установки
echo "⚙️ Запуск установочного скрипта..."
run_remote "cd /tmp/FormaContact && chmod +x setup_ubuntu.sh && sudo ./setup_ubuntu.sh"

echo ""
echo "✅ Установка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Подключитесь к серверу: ssh $SERVER_USER@$SERVER_IP"
echo "2. Отредактируйте конфигурацию: sudo nano /opt/telegram_bot/.env"
echo "3. Добавьте ваши данные:"
echo "   BOT_TOKEN=ваш_реальный_токен"
echo "   ADMIN_CHAT_ID=ваш_реальный_chat_id"
echo "4. Запустите бота: sudo systemctl start telegram-bot"
echo "5. Проверьте статус: sudo systemctl status telegram-bot"
echo ""
echo "🔧 Полезные команды на сервере:"
echo "   sudo systemctl status telegram-bot    # Статус"
echo "   sudo systemctl restart telegram-bot   # Перезапуск"
echo "   sudo journalctl -u telegram-bot -f    # Логи"
echo ""

# Опциональная автоматическая настройка (если есть данные)
read -p "🤖 Хотите автоматически настроить переменные окружения? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Введите BOT_TOKEN: " BOT_TOKEN
    read -p "Введите ADMIN_CHAT_ID: " ADMIN_CHAT_ID
    
    if [ ! -z "$BOT_TOKEN" ] && [ ! -z "$ADMIN_CHAT_ID" ]; then
        echo "📝 Настройка переменных окружения..."
        run_remote "sudo tee /opt/telegram_bot/.env > /dev/null <<EOF
BOT_TOKEN=$BOT_TOKEN
ADMIN_CHAT_ID=$ADMIN_CHAT_ID
EOF"
        
        echo "🚀 Запуск бота..."
        run_remote "sudo systemctl start telegram-bot"
        run_remote "sudo systemctl enable telegram-bot"
        
        echo "📊 Проверка статуса..."
        run_remote "sudo systemctl status telegram-bot --no-pager"
        
        echo ""
        echo "🎉 Бот запущен и настроен!"
        echo "📱 Проверьте работу бота в Telegram"
    else
        echo "⚠️ Не все данные введены. Настройте вручную."
    fi
fi

echo ""
echo "🎯 Развертывание завершено!"
echo "🌐 Ссылка на репозиторий: $REPO_URL" 