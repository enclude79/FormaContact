#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print("❌ Ошибка: BOT_TOKEN не найден в переменных окружения")
    exit(1)

async def get_bot_info():
    """Получаем информацию о боте"""
    bot = Bot(token=BOT_TOKEN)
    
    try:
        # Получаем информацию о боте
        bot_info = await bot.get_me()
        
        print("🤖 Информация о боте:")
        print(f"ID: {bot_info.id}")
        print(f"Имя: {bot_info.first_name}")
        print(f"Username: @{bot_info.username}")
        print(f"Ссылка: https://t.me/{bot_info.username}")
        print(f"Ссылка с автостартом: https://t.me/{bot_info.username}?start=form")
        
        return bot_info.username
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(get_bot_info()) 