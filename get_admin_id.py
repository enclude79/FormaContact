#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print("❌ Ошибка: BOT_TOKEN не найден в переменных окружения")
    exit(1)

async def get_admin_chat_id():
    """Получаем Chat ID администратора из последних обновлений"""
    bot = Bot(BOT_TOKEN)
    
    try:
        updates = await bot.get_updates()
        
        if updates:
            print("🔍 Найденные чаты:")
            print("-" * 50)
            
            unique_chats = {}
            for update in updates:
                if update.message:
                    chat_id = update.message.chat.id
                    user = update.message.from_user
                    
                    if chat_id not in unique_chats:
                        unique_chats[chat_id] = {
                            'first_name': user.first_name,
                            'last_name': user.last_name or '',
                            'username': user.username or 'no_username',
                            'message_count': 1
                        }
                    else:
                        unique_chats[chat_id]['message_count'] += 1
            
            for chat_id, info in unique_chats.items():
                print(f"Chat ID: {chat_id}")
                print(f"Имя: {info['first_name']} {info['last_name']}")
                print(f"Username: @{info['username']}")
                print(f"Сообщений: {info['message_count']}")
                print("-" * 50)
                
            if unique_chats:
                # Берем первый найденный Chat ID
                admin_chat_id = list(unique_chats.keys())[0]
                print(f"\n✅ Рекомендуемый ADMIN_CHAT_ID: {admin_chat_id}")
                return admin_chat_id
        else:
            print("❌ Нет сообщений. Напишите боту любое сообщение и запустите скрипт снова.")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

if __name__ == "__main__":
    admin_id = asyncio.run(get_admin_chat_id()) 