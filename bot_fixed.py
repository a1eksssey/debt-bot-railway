#!/usr/bin/env python3
"""ИСПРАВЛЕННАЯ версия бота"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получаем настройки
TOKEN = os.getenv("TELEGRAM_TOKEN", "")

# ==================== HANDLERS ====================

async def start(update: Update, context):
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton("📊 Проверить работу", callback_data='test')],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "✅ Бот работает!\n"
        "Выберите действие:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'test':
        await query.edit_message_text("✅ Кнопки работают!\nБот полностью функционирует.")
    elif query.data == 'help':
        await query.edit_message_text(
            "📖 **Помощь**\n\n"
            "Бот учета долгов успешно запущен на Railway.\n"
            "Следующий шаг - подключение Google Sheets.",
            parse_mode='Markdown'
        )

def main():
    """Запуск бота"""
    if not TOKEN:
        print("❌ Ошибка: Токен бота не найден!")
        return
    
    # Создаем приложение
    app = Application.builder().token(TOKEN).build()
    
    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # Запускаем бота
    print("=" * 50)
    print("🤖 Бот запущен!")
    print(f"Токен: {TOKEN[:10]}...")
    print("=" * 50)
    
    app.run_polling()

if __name__ == "__main__":
    main()