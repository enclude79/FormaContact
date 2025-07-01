#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Конфигурация
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print("❌ Ошибка: BOT_TOKEN не найден в переменных окружения")
    exit(1)
    
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def test_bot():
    """Тестирование доступности бота"""
    
    print("🔍 Тестирование Telegram бота...")
    
    # 1. Проверка токена
    try:
        response = requests.get(f"{BASE_URL}/getMe")
        data = response.json()
        
        if data['ok']:
            bot_info = data['result']
            print(f"✅ Бот найден: @{bot_info['username']} ({bot_info['first_name']})")
            print(f"   ID: {bot_info['id']}")
            print(f"   Может получать сообщения: {'Да' if bot_info.get('can_read_all_group_messages', False) else 'Нет'}")
        else:
            print(f"❌ Ошибка: {data['description']}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка подключения к Telegram API: {e}")
        return False
    
    # 2. Проверка последних обновлений
    try:
        response = requests.get(f"{BASE_URL}/getUpdates")
        data = response.json()
        
        if data['ok']:
            updates = data['result']
            print(f"📬 Получено обновлений: {len(updates)}")
            
            if updates:
                last_update = updates[-1]
                print(f"   Последнее обновление ID: {last_update['update_id']}")
                if 'message' in last_update:
                    msg = last_update['message']
                    print(f"   От: {msg.get('from', {}).get('first_name', 'Неизвестно')}")
                    print(f"   Текст: {msg.get('text', 'Нет текста')}")
        else:
            print(f"❌ Ошибка получения обновлений: {data['description']}")
            
    except Exception as e:
        print(f"❌ Ошибка получения обновлений: {e}")
    
    # 3. Тест отправки сообщения самому себе (админу)
    admin_chat_id = os.getenv('ADMIN_CHAT_ID')
    if not admin_chat_id:
        print("❌ Ошибка: ADMIN_CHAT_ID не найден в переменных окружения")
        return False
        
    test_message = "🧪 Тестовое сообщение от бота"
    
    try:
        response = requests.post(f"{BASE_URL}/sendMessage", {
            'chat_id': admin_chat_id,
            'text': test_message,
            'parse_mode': 'Markdown'
        })
        data = response.json()
        
        if data['ok']:
            print(f"✅ Тестовое сообщение отправлено админу (ID: {admin_chat_id})")
        else:
            print(f"❌ Ошибка отправки сообщения: {data['description']}")
            
    except Exception as e:
        print(f"❌ Ошибка отправки тестового сообщения: {e}")
    
    print("\n📋 Результат тестирования:")
    print("   ✅ Бот доступен и работает")
    print("   📱 Проверьте Telegram - должно прийти тестовое сообщение")
    print("   🔧 Если бот не отвечает на команды, перезапустите telegram_bot.py")
    
    return True

if __name__ == '__main__':
    test_bot() 