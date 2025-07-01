#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from telegram import Bot
from telegram.ext import Application, MessageHandler, filters
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print("❌ Ошибка: BOT_TOKEN не найден в переменных окружения")
    exit(1)

async def get_chat_id(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user
    print(f'Chat ID: {chat_id}')
    print(f'User: {user.first_name} {user.last_name or ""} (@{user.username or "no_username"})')
    await update.message.reply_text(f'Ваш Chat ID: {chat_id}')

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, get_chat_id))
    
    print('Бот запущен. Отправьте любое сообщение боту для получения Chat ID...')
    app.run_polling()

if __name__ == '__main__':
    main() 