#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
import traceback
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import re

# Загрузка переменных окружения
load_dotenv()

# Создание директории для логов
logs_dir = '/home/enclude/FormaContact/logs'
os.makedirs(logs_dir, exist_ok=True)

# Улучшенная настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{logs_dir}/bot.log', encoding='utf-8'),
        logging.FileHandler(f'{logs_dir}/bot_errors.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Настройка логгера для ошибок
error_logger = logging.getLogger('errors')
error_handler = logging.FileHandler(f'{logs_dir}/bot_errors.log', encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s - ERROR - %(message)s')
error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)

logger = logging.getLogger(__name__)

# Конфигурация из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

# Проверка наличия обязательных переменных
if not BOT_TOKEN:
    logger.error("BOT_TOKEN не найден в переменных окружения")
    raise ValueError("BOT_TOKEN не найден в переменных окружения")

# Хранилище состояний пользователей
user_data = {}
admin_chat_ids = set()  # Для хранения потенциальных админов

async def error_handler_func(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    error_msg = f"Exception while handling an update: {context.error}"
    logger.error(error_msg)
    error_logger.error(f"{error_msg}\nUpdate: {update}\nTraceback: {traceback.format_exc()}")
    
    # Если есть update и это сообщение
    if update and hasattr(update, 'effective_message') and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "🆘 Произошла ошибка! Администраторы уже уведомлены. 🆘"
            )
        except Exception:
            pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_info = f"@{update.effective_user.username or 'no_username'} ({update.effective_user.first_name})"
    
    # Проверяем параметры deep linking
    start_param = None
    if context.args:
        start_param = context.args[0]
        logger.info(f"🔗 Deep link параметр: {start_param}")
    
    logger.info(f"🚀 Команда /start от пользователя {user_id} ({user_info}), Chat ID: {chat_id}")
    
    # Сохраняем потенциальных админов
    admin_chat_ids.add(chat_id)
    
    # Логируем Chat ID для администратора (только в логи)
    logger.info(f"📝 Chat ID для настройки: {chat_id}")
    
    user_data[user_id] = {}
    
    # Если пользователь пришел по ссылке с параметром, сразу показываем форму заявки
    if start_param in ['form', 'request', 'application']:
        user_data[user_id] = {'step': 'waiting_name'}
        try:
            await update.message.reply_text(
                "🌟 *ДОБРО ПОЖАЛОВАТЬ! ДАВАЙТЕ ОФОРМИМ ЗАЯВКУ!* 🌟\n\n"
                "✨ Для начала введите ваше имя:\n"
                "💫 Мы хотим знать, как к вам обращаться! 💫",
                parse_mode='Markdown'
            )
            logger.info(f"✅ Автоматический запуск формы для пользователя {user_id}")
            return
        except Exception as e:
            logger.error(f"❌ Ошибка автоматического запуска формы: {e}")
    
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
    
    try:
        await update.message.reply_text(
            welcome_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        logger.info(f"✅ Приветствие отправлено пользователю {user_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки приветствия: {e}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_info = f"@{query.from_user.username or 'no_username'} ({query.from_user.first_name})"
    
    logger.info(f"🔘 Нажата кнопка '{query.data}' пользователем {user_id} ({user_info})")
    
    if query.data == 'new_request':
        user_data[user_id] = {'step': 'waiting_name'}
        try:
            await query.edit_message_text(
                "🌟 *КАК ВАС ЗОВУТ?* 🌟\n\n"
                "✨ Введите ваше прекрасное имя:\n"
                "💫 Мы хотим знать, как к вам обращаться! 💫",
                parse_mode='Markdown'
            )
            logger.info(f"✅ Запрос имени отправлен пользователю {user_id}")
        except Exception as e:
            logger.error(f"❌ Ошибка отправки запроса имени: {e}")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    message_text = update.message.text
    user_info = f"@{update.effective_user.username or 'no_username'} ({update.effective_user.first_name})"
    
    logger.info(f"📨 Сообщение от {user_id} ({user_info}): '{message_text[:100]}...'")
    
    # Добавляем Chat ID в список потенциальных админов
    admin_chat_ids.add(chat_id)
    
    if user_id not in user_data:
        try:
            await update.message.reply_text(
                "🌈 Давайте начнем с команды /start! 🌈\n✨ Приключение ждет! ✨"
            )
            logger.info(f"✅ Предложение старта отправлено пользователю {user_id}")
        except Exception as e:
            logger.error(f"❌ Ошибка отправки предложения старта: {e}")
        return
    
    current_step = user_data[user_id].get('step')
    
    if current_step == 'waiting_name':
        # Валидация имени
        if len(message_text.strip()) < 2:
            try:
                await update.message.reply_text(
                    "🎭 Упс! Имя должно быть длиннее! 🎭\n"
                    "✨ Введите имя минимум из 2 символов ✨\n"
                    "💫 Мы верим в вас! 💫"
                )
                logger.warning(f"⚠️ Некорректное имя от пользователя {user_id}: '{message_text}'")
            except Exception as e:
                logger.error(f"❌ Ошибка отправки сообщения об ошибке имени: {e}")
            return
        
        user_data[user_id]['name'] = message_text.strip()
        user_data[user_id]['step'] = 'waiting_phone'
        
        logger.info(f"✅ Имя получено от пользователя {user_id}: '{message_text.strip()}'")
        
        try:
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
            logger.info(f"✅ Запрос телефона отправлен пользователю {user_id}")
        except Exception as e:
            logger.error(f"❌ Ошибка отправки запроса телефона: {e}")
    
    elif current_step == 'waiting_phone':
        # Валидация телефона
        phone = clean_phone(message_text)
        if not is_valid_phone(phone):
            try:
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
                logger.warning(f"⚠️ Некорректный телефон от пользователя {user_id}: '{message_text}'")
            except Exception as e:
                logger.error(f"❌ Ошибка отправки сообщения об ошибке телефона: {e}")
            return
        
        user_data[user_id]['phone'] = format_phone(phone)
        
        # Формируем заявку
        name = user_data[user_id]['name']
        phone_formatted = user_data[user_id]['phone']
        username = update.effective_user.username
        user_full_name = f"{update.effective_user.first_name or ''} {update.effective_user.last_name or ''}".strip()
        
        logger.info(f"📋 Новая заявка от {user_id}: Имя='{name}', Телефон='{phone_formatted}'")
        
        # Отправляем заявку администратору
        admin_message = f"""🎊 НОВАЯ ГОРЯЧАЯ ЗАЯВКА! 🎊

🌟 Имя: {name}
📱 Телефон: {phone_formatted}
🆔 User ID: {user_id}
👤 Telegram: @{username or 'не указан'} ({user_full_name})
🗨️ Chat ID: {chat_id}
⏰ Время: {update.message.date.strftime('%d.%m.%Y %H:%M:%S')}

🚀 Клиент готов к сотрудничеству! 🚀
💎 Действуйте быстро! 💎"""
        
        # Попытка отправки всем потенциальным админам
        admin_sent = False
        if ADMIN_CHAT_ID and ADMIN_CHAT_ID.isdigit():
            try:
                await context.bot.send_message(
                    chat_id=int(ADMIN_CHAT_ID),
                    text=admin_message
                )
                logger.info(f"✅ Заявка отправлена админу {ADMIN_CHAT_ID}")
                admin_sent = True
            except Exception as e:
                logger.error(f"❌ Ошибка отправки заявки админу {ADMIN_CHAT_ID}: {e}")
        
        # Если не удалось отправить админу, отправляем всем известным чатам
        if not admin_sent:
            logger.warning("⚠️ ADMIN_CHAT_ID не настроен или недоступен, отправка заявки всем известным чатам")
            for admin_id in admin_chat_ids:
                try:
                    # Проверяем, не отправляем ли заявку самому заявителю
                    if admin_id != chat_id:
                        await context.bot.send_message(
                            chat_id=admin_id,
                            text=admin_message
                        )
                        logger.info(f"✅ Заявка отправлена потенциальному админу {admin_id}")
                        admin_sent = True
                    else:
                        # Если это сам заявитель, записываем в логи для настройки
                        logger.warning(f"📝 НАСТРОЙКА: Установите ADMIN_CHAT_ID={admin_id} в .env файле для получения заявок")
                except Exception as e:
                    logger.error(f"❌ Ошибка отправки заявки потенциальному админу {admin_id}: {e}")
        
        try:
            # Подтверждение пользователю
            await update.message.reply_text(
                "🎉 *ПОТРЯСАЮЩЕ! ЗАЯВКА ПРИНЯТА!* 🎉\n\n"
                "✨ *Ваши данные:* ✨\n"
                f"🌟 **Имя:** {name}\n"
                f"📱 **Телефон:** {phone_formatted}\n\n"
                "🚀 *Что дальше?*\n"
                "💫 Наш супер-специалист уже мчится к телефону!\n"
                "🔥 Скоро получите звонок с эксклюзивным предложением!\n"
                "💎 Приготовьтесь к удивительным возможностям!\n\n"
                "🌈 Хотите оставить еще одну заявку? Жмите /start! 🌈\n"
                "✨ Мы всегда рады помочь! ✨",
                parse_mode='Markdown'
            )
            logger.info(f"✅ Подтверждение отправлено пользователю {user_id}")
            
            # Очищаем данные пользователя
            del user_data[user_id]
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки подтверждения: {e}")
            try:
                await update.message.reply_text(
                    "🆘 Упс! Произошла техническая заминка! 🆘\n"
                    "🔧 Наши программисты уже чинят это!\n"
                    "💫 Попробуйте через минутку или напишите администратору! 💫\n"
                    "🌟 Мы обязательно вам поможем! 🌟"
                )
            except Exception as e2:
                logger.error(f"❌ Критическая ошибка отправки сообщения об ошибке: {e2}")

def clean_phone(phone_str):
    """Очистка номера телефона от лишних символов"""
    return re.sub(r'[^\d+]', '', phone_str)

def is_valid_phone(phone):
    """Валидация номера телефона"""
    # Российские номера: 7XXXXXXXXXX, 8XXXXXXXXXX, или международные +XXXXXXXXXXXXX
    patterns = [
        r'^\+?7\d{10}$',  # +7XXXXXXXXXX или 7XXXXXXXXXX
        r'^8\d{10}$',     # 8XXXXXXXXXX 
        r'^\d{10}$',      # XXXXXXXXXX (будет +7)
        r'^\+\d{7,15}$'   # Международные +XXXXXXXXXXXXX
    ]
    
    for pattern in patterns:
        if re.match(pattern, phone):
            return True
    return False

def format_phone(phone):
    """Форматирование номера телефона"""
    # Убираем все кроме цифр и +
    clean = re.sub(r'[^\d+]', '', phone)
    
    # Российские номера
    if clean.startswith('8') and len(clean) == 11:
        return '+7' + clean[1:]
    elif clean.startswith('7') and len(clean) == 11:
        return '+' + clean
    elif clean.startswith('+7') and len(clean) == 12:
        return clean
    elif len(clean) == 10:  # Номер без кода страны
        return '+7' + clean
    elif clean.startswith('+'):
        return clean
    else:
        return '+' + clean

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    logger.info(f"ℹ️ Команда /help от пользователя {user_id}")
    
    help_text = f"""
🔧 *ПОМОЩЬ ПО БОТУ FORMACONTACT* 🔧

🚀 *Команды:*
/start - Начать работу с ботом
/help - Показать эту справку

🆔 *Ваш Chat ID:* `{chat_id}`

📋 *Как пользоваться:*
1. Нажмите /start
2. Нажмите кнопку "Оставить заявку"
3. Введите ваше имя
4. Введите номер телефона
5. Готово! Ждите звонка!

📞 *Поддерживаемые форматы телефонов:*
🇷🇺 Россия: +7, 8, 7
🌍 Международные: +код страны

💬 *По вопросам пишите администратору*
    """
    
    try:
        await update.message.reply_text(help_text, parse_mode='Markdown')
        logger.info(f"✅ Справка отправлена пользователю {user_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки справки: {e}")

def main() -> None:
    """Запуск бота"""
    logger.info("🎉 Telegram бот FormaContact с улучшенным логированием запускается! 🎉")
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler_func)
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    logger.info("✅ Все обработчики зарегистрированы")
    logger.info(f"🆔 Потенциальные админ чаты: {list(admin_chat_ids)}")
    
    # Запускаем бот
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"💥 Критическая ошибка запуска бота: {e}")
        error_logger.error(f"Критическая ошибка: {traceback.format_exc()}")
        raise

if __name__ == '__main__':
    main()