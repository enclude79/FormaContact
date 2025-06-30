#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

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
    """Форматирование номера телефона"""
    digits_only = clean_phone(phone).lstrip('+')
    
    # Конвертируем 8 в 7
    if digits_only.startswith('8') and len(digits_only) == 11:
        digits_only = '7' + digits_only[1:]
    
    # Добавляем код страны для мобильных номеров
    elif len(digits_only) == 10 and digits_only.startswith('9'):
        digits_only = '7' + digits_only
    
    # Форматируем только если 11 цифр и начинается с 7
    if len(digits_only) == 11 and digits_only.startswith('7'):
        return f"+7 ({digits_only[1:4]}) {digits_only[4:7]}-{digits_only[7:9]}-{digits_only[9:11]}"
    
    # Возвращаем исходный номер если не удалось отформатировать
    return phone

def test_phone_validation():
    """Тестирование валидации номеров телефона"""
    
    print("🧪 Тестирование валидации номеров телефона\n")
    
    # Тестовые случаи
    test_cases = [
        # Корректные российские номера
        ("+7 916 123 45 67", True, "Российский номер с +7"),
        ("8 (916) 123-45-67", True, "Российский номер с 8"),
        ("79161234567", True, "Российский номер без пробелов с 7"),
        ("9161234567", True, "Российский мобильный без кода страны"),
        ("+7 916 386 33 03", True, "Корректный российский номер"),
        
        # Корректные международные номера
        ("+380 67 123 45 67", True, "Украинский номер"),
        ("+1 555 123 4567", True, "Американский номер"),
        ("+49 30 12345678", True, "Немецкий номер"),
        ("+33 1 42 34 56 78", True, "Французский номер"),
        ("+86 138 0013 8000", True, "Китайский номер"),
        ("12345678901", True, "Международный без +"),
        ("+44 20 7946 0958", True, "Британский номер"),
        
        # Некорректные номера
        ("+7 916 386 33 0", False, "Неполный российский номер"),
        ("+7 916 386 3", False, "Очень короткий номер"),
        ("123456", False, "Слишком короткий (6 цифр)"),
        ("1234567890123456", False, "Слишком длинный (16 цифр)"),
        ("", False, "Пустая строка"),
        ("abc", False, "Буквы"),
        ("+", False, "Только плюс"),
        ("++123456789", False, "Двойной плюс"),
    ]
    
    print("Результаты тестирования:")
    print("-" * 80)
    
    for phone, expected, description in test_cases:
        cleaned = clean_phone(phone)
        is_valid = is_valid_phone(cleaned)
        
        if is_valid:
            formatted = format_phone(cleaned)
        else:
            formatted = "❌ Некорректный"
        
        status = "✅" if is_valid == expected else "❌"
        
        print(f"{status} {description}")
        print(f"   Входной:     '{phone}'")
        print(f"   Очищенный:   '{cleaned}'")
        print(f"   Валидный:    {is_valid}")
        print(f"   Ожидаемый:   {expected}")
        print(f"   Форматированный: {formatted}")
        print()

if __name__ == '__main__':
    test_phone_validation() 
 