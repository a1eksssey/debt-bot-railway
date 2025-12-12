#!/usr/bin/env python3
"""
Упрощенная версия бота для учета долгов
"""

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
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
ADMIN_IDS = os.getenv("ADMIN_IDS", "283883536,222222222").split(',')

# ==================== HANDLERS ====================

async def start(update: Update, context):
    """Обработчик команды /start"""
    user_id = update.effective_user.id
    
    # Проверяем админа
    if str(user_id) in ADMIN_IDS:
        keyboard = [
            [InlineKeyboardButton("👥 Общая сумма долгов", callback_data='all_debts')],
            [InlineKeyboardButton("👤 Долг сотрудника", callback_data='employee_debt')],
            [InlineKeyboardButton("ℹ️ Справка", callback_data='help')]
        ]
        text = "👑 Администратор\nВыберите действие:"
    else:
        keyboard = [
            [InlineKeyboardButton("📊 Мой долг", callback_data='my_debt')],
            [InlineKeyboardButton("📅 Долг за день", callback_data='daily_debt')],
            [InlineKeyboardButton("ℹ️ Справка", callback_data='help')]
        ]
        text = "👤 Сотрудник\nВыберите действие:"
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

async def button_handler(update: Update, context):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    is_admin = str(user_id) in ADMIN_IDS
    
    if query.data == 'help':
        await query.edit_message_text(
            "📖 **Справка по боту учета долгов**\n\n"
            "Бот находится в разработке.\n"
            "Скоро будут добавлены:\n"
            "• Подключение к Google Sheets\n"
            "• Расчет долгов\n"
            "• Уведомления\n\n"
            "Версия 1.0",
            parse_mode='Markdown'
        )
    elif query.data == 'all_debts' and is_admin:
        await query.edit_message_text(
            "👥 **Общая сумма долгов**\n\n"
            "Функция в разработке.\n"
            "Скоро здесь будет отображаться сумма долгов всех сотрудников."
        )
    elif query.data == 'employee_debt' and is_admin:
        await query.edit_message_text(
            "👤 **Долг сотрудника**\n\n"
            "Функция в разработке.\n"
            "Скоро здесь можно будет проверить долг любого сотрудника."
        )
    elif query.data == 'my_debt' and not is_admin:
        await query.edit_message_text(
            "📊 **Ваш долг**\n\n"
            "Функция в разработке.\n"
            "Скоро здесь будет отображаться ваш текущий долг."
        )
    elif query.data == 'daily_debt' and not is_admin:
        await query.edit_message_text(
            "📅 **Долг за день**\n\n"
            "Функция в разработке.\n"
            "Скоро здесь можно будет посмотреть долг за конкретный день."
        )
    else:
        await query.edit_message_text("⛔ У вас нет доступа к этой функции")

async def echo(update: Update, context):
    """Повторяет сообщение пользователя"""
    await update.message.reply_text(f"Вы сказали: {update.message.text}")

def main():
    """Запуск бота"""
    if not TELEGRAM_TOKEN:
        print("❌ Ошибка: Токен бота не найден!")
        print("Добавьте TELEGRAM_TOKEN в настройки Railway")
        return
    
    # Создаем приложение
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("help", start))
    
    # Запускаем бота
    print("🤖 Бот запускается...")
    app.run_polling()

if __name__ == "__main__":
    main()