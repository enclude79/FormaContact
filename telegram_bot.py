#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import re

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID'))

# Проверка наличия обязательных переменных
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения")
if not ADMIN_CHAT_ID:
    raise ValueError("ADMIN_CHAT_ID не найден в переменных окружения")

# Хранилище состояний пользователей
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user_id = update.effective_user.id
    user_data[user_id] = {}
    
    keyboard = [
        [InlineKeyboardButton("🌟 Оставить заявку 🌟", callback_data='new_request')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = """
🎉 *ДОБРО ПОЖАЛОВАТЬ В МИР НЕДВИЖИМОСТИ!* 🎉

🏡✨ Ваш личный помощник по анализу недвижимости ждет вас! ✨🏡

🌈 Что мы предлагаем:
🔥 Профессиональные консультации
💎 Эксклюзивные предложения  
🚀 Быстрый анализ рынка
🎯 Персональный подход

💫 Готовы начать путешествие в мир недвижимости? 💫
Жмите яркую кнопку ниже! 👇✨
    """
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == 'new_request':
        user_data[user_id] = {'step': 'waiting_name'}
        await query.edit_message_text(
            "🌟 *КАК ВАС ЗОВУТ?* 🌟\n\n"
            "✨ Введите ваше прекрасное имя:\n"
            "💫 Мы хотим знать, как к вам обращаться! 💫",
            parse_mode='Markdown'
        )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    if user_id not in user_data:
        await update.message.reply_text(
            "🌈 Давайте начнем с команды /start! 🌈\n✨ Приключение ждет! ✨"
        )
        return
    
    current_step = user_data[user_id].get('step')
    
    if current_step == 'waiting_name':
        # Валидация имени
        if len(message_text.strip()) < 2:
            await update.message.reply_text(
                "🎭 Упс! Имя должно быть длиннее! 🎭\n"
                "✨ Введите имя минимум из 2 символов ✨\n"
                "💫 Мы верим в вас! 💫"
            )
            return
        
        user_data[user_id]['name'] = message_text.strip()
        user_data[user_id]['step'] = 'waiting_phone'
        
        await update.message.reply_text(
            "🎯 *ОТЛИЧНО! ТЕПЕРЬ ТЕЛЕФОН!* 🎯\n\n"
            "📱 Укажите номер телефона для связи:\n\n"
            "🇷🇺 *Российские номера:*\n"
            "🌟 +7 916 123 45 67\n"
            "🌟 8 (916) 123-45-67\n"
            "🌟 79161234567\n"
            "🌟 9161234567\n\n"
            "🌍 *Международные номера:*\n"
            "🔥 +380 67 123 45 67 (Украина)\n"
            "🔥 +1 555 123 4567 (США/Канада)\n"
            "🔥 +49 30 12345678 (Германия)\n"
            "🔥 +33 1 42 86 83 26 (Франция)\n"
            "🔥 +86 138 0013 8000 (Китай)\n"
            "🔥 +44 20 7946 0958 (Великобритания)",
            parse_mode='Markdown'
        )
    
    elif current_step == 'waiting_phone':
        # Валидация телефона
        phone = clean_phone(message_text)
        if not is_valid_phone(phone):
            await update.message.reply_text(
                "🚨 УПС! ЧТО-ТО ПОШЛО НЕ ТАК! 🚨\n\n"
                "💡 *Требования к номеру:*\n"
                "🎯 От 7 до 15 цифр\n"
                "🎯 Только цифры и символ +\n"
                "🎯 Российские или международные номера\n\n"
                "🌟 *Попробуйте эти форматы:*\n"
                "🇷🇺 *Россия:*\n"
                "💫 +7 916 123 45 67\n"
                "💫 8 (916) 123-45-67\n"
                "💫 79161234567\n\n"
                "🌍 *Мир:*\n"
                "🔥 +380 67 123 45 67 (Украина)\n"
                "🔥 +1 555 123 4567 (США)\n"
                "🔥 +49 30 12345678 (Германия)\n"
                "🔥 +86 138 0013 8000 (Китай)\n\n"
                "💪 Попробуйте еще раз! У вас получится! 💪"
            )
            return
        
        user_data[user_id]['phone'] = format_phone(phone)
        
        # Формируем заявку
        name = user_data[user_id]['name']
        phone = user_data[user_id]['phone']
        username = update.effective_user.username
        user_full_name = f"{update.effective_user.first_name or ''} {update.effective_user.last_name or ''}".strip()
        
        # Отправляем заявку администратору
        admin_message = f"""🎊 НОВАЯ ГОРЯЧАЯ ЗАЯВКА! 🎊

🌟 Имя: {name}
📱 Телефон: {phone}
🆔 User ID: {user_id}
👤 Telegram: @{username or 'не указан'} ({user_full_name})
⏰ Время: {update.message.date.strftime('%d.%m.%Y %H:%M:%S')}

🚀 Клиент готов к сотрудничеству! 🚀
💎 Действуйте быстро! 💎"""
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_message
            )
            
            # Подтверждение пользователю
            await update.message.reply_text(
                "🎉 *ПОТРЯСАЮЩЕ! ЗАЯВКА ПРИНЯТА!* 🎉\n\n"
                "✨ *Ваши данные:* ✨\n"
                f"🌟 **Имя:** {name}\n"
                f"📱 **Телефон:** {phone}\n\n"
                "🚀 *Что дальше?*\n"
                "💫 Наш супер-специалист уже мчится к телефону!\n"
                "🔥 Скоро получите звонок с эксклюзивным предложением!\n"
                "💎 Приготовьтесь к удивительным возможностям!\n\n"
                "🌈 Хотите оставить еще одну заявку? Жмите /start! 🌈\n"
                "✨ Мы всегда рады помочь! ✨",
                parse_mode='Markdown'
            )
            
            # Очищаем данные пользователя
            del user_data[user_id]
            
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения админу: {e}")
            await update.message.reply_text(
                "🆘 Упс! Произошла техническая заминка! 🆘\n"
                "🔧 Наши программисты уже чинят это!\n"
                "💫 Попробуйте через минутку или напишите администратору! 💫\n"
                "🌟 Мы обязательно вам поможем! 🌟"
            )

def clean_phone(phone_str):
    """Очистка номера телефона от лишних символов"""
    return re.sub(r'[^\d+]', '', phone_str)

def is_valid_phone(phone):
    """Проверка корректности номера телефона"""
    # Убираем + в начале для проверки
    digits_only = phone.lstrip('+')
    
    # Проверяем что содержит только цифры
    if not digits_only.isdigit():
        return False
    
    # Минимальная длина для международных номеров - 7 цифр
    # Максимальная длина - 15 цифр (международный стандарт E.164)
    if len(digits_only) < 7 or len(digits_only) > 15:
        return False
    
    # Российские номера - строгая проверка
    if phone.startswith('+7'):
        return len(digits_only) == 11
    elif phone.startswith('8'):
        return len(digits_only) == 11
    elif phone.startswith('7') and not phone.startswith('+'):
        return len(digits_only) == 11
    elif len(digits_only) == 10 and digits_only.startswith('9'):  # российский мобильный без кода
        return True
    
    # Международные номера с + в начале
    elif phone.startswith('+') and len(digits_only) >= 7:
        return True
    
    # Номера без + но с международным кодом (начинается не с 7, 8, 9)
    elif len(digits_only) >= 10 and not digits_only.startswith(('7', '8', '9')):
        return True
    
    return False

def format_phone(phone):
    """Форматирование номера телефона для красивого отображения"""
    # Убираем + в начале для обработки
    digits_only = phone.lstrip('+')
    
    # Российские номера
    if phone.startswith('+7') or (phone.startswith('8') and len(digits_only) == 11):
        if phone.startswith('8'):
            digits_only = '7' + digits_only[1:]  # заменяем 8 на 7
        elif phone.startswith('7') and not phone.startswith('+'):
            pass  # digits_only уже правильный
        elif len(digits_only) == 10 and digits_only.startswith('9'):
            digits_only = '7' + digits_only  # добавляем код России
        
        # Форматируем российский номер: +7 (XXX) XXX-XX-XX
        if len(digits_only) == 11 and digits_only.startswith('7'):
            return f"+7 ({digits_only[1:4]}) {digits_only[4:7]}-{digits_only[7:9]}-{digits_only[9:11]}"
    
    # Международные номера - возвращаем с + в начале без дополнительного форматирования
    if not phone.startswith('+'):
        return '+' + digits_only
    
    return phone

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = """
🌈 *СПРАВКА ПО БОТУ* 🌈

🎯 *Доступные команды:*
🌟 /start - Начать работу с ботом
🌟 /help - Показать эту справку

🚀 *Как пользоваться:*
💫 Нажмите /start
💫 Нажмите кнопку "Оставить заявку"
💫 Введите ваше имя
💫 Укажите номер телефона
💫 Готово! Мы свяжемся с вами!

🔥 *Поддерживаемые форматы телефонов:*
🇷🇺 Российские: +7, 8, или просто мобильный номер
🌍 Международные: любые номера с кодом страны

💎 Вопросы? Пишите администратору! 💎
✨ Мы всегда готовы помочь! ✨
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main() -> None:
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # Запускаем бота
    logger.info("🎉 Telegram бот с яркими красками запущен! 🎉")
    application.run_polling()

if __name__ == '__main__':
    main()