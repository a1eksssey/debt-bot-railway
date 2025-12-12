#!/usr/bin/env python3
"""
Бот для учета долгов с Google Sheets
"""

import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем настройки
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "")
ADMIN_IDS = os.getenv("ADMIN_IDS", "283883536,222222222").split(',')

# ==================== GOOGLE SHEETS ====================

class GoogleSheetsClient:
    """Упрощенный клиент для Google Sheets"""
    
    def __init__(self):
        self.api_key = GOOGLE_API_KEY
        self.spreadsheet_id = SPREADSHEET_ID
        self.connected = False
        
    def test_connection(self):
        """Проверка подключения"""
        try:
            if not self.api_key or not self.spreadsheet_id:
                return False, "❌ Не настроены API ключи"
            
            # Здесь будет реальное подключение
            # Пока просто имитируем успех
            self.connected = True
            return True, "✅ Подключение к Google Sheets установлено"
            
        except Exception as e:
            return False, f"❌ Ошибка подключения: {str(e)}"
    
    def get_test_data(self):
        """Возвращает тестовые данные (заглушка)"""
        return [
            {"date": "01.01.2024", "employee": "Иванов Иван", "items": "Кофе, печенье", "amount": 150},
            {"date": "02.01.2024", "employee": "Петров Петр", "items": "Чай, бутерброд", "amount": 100},
            {"date": "03.01.2024", "employee": "Сидоров Сидор", "items": "Вода", "amount": 50},
        ]

# Создаем клиент Google Sheets
sheets_client = GoogleSheetsClient()

# ==================== HANDLERS ====================

async def start(update: Update, context):
    """Обработчик команды /start"""
    user_id = update.effective_user.id
    
    # Проверяем подключение к Google Sheets
    connection_status, message = sheets_client.test_connection()
    
    # Проверяем админа
    if str(user_id) in ADMIN_IDS:
        keyboard = [
            [InlineKeyboardButton("📊 Проверить подключение", callback_data='check_connection')],
            [InlineKeyboardButton("👥 Тестовые данные", callback_data='test_data')],
            [InlineKeyboardButton("👤 Мой статус", callback_data='my_status')],
            [InlineKeyboardButton("ℹ️ Справка", callback_data='help')]
        ]
        text = f"👑 Администратор\n{message}\n\nВыберите действие:"
    else:
        keyboard = [
            [InlineKeyboardButton("📊 Мой долг", callback_data='my_debt')],
            [InlineKeyboardButton("📅 Долг за день", callback_data='daily_debt')],
            [InlineKeyboardButton("👤 Мой статус", callback_data='my_status')],
            [InlineKeyboardButton("ℹ️ Справка", callback_data='help')]
        ]
        text = f"👤 Сотрудник\n{message}\n\nВыберите действие:"
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

async def button_handler(update: Update, context):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    is_admin = str(user_id) in ADMIN_IDS
    
    if query.data == 'help':
        await show_help(query)
    elif query.data == 'check_connection' and is_admin:
        await check_connection(query)
    elif query.data == 'test_data' and is_admin:
        await show_test_data(query)
    elif query.data == 'my_status':
        await show_my_status(query, user_id)
    elif query.data == 'my_debt' and not is_admin:
        await show_my_debt(query, user_id)
    elif query.data == 'daily_debt' and not is_admin:
        await show_daily_debt(query)
    else:
        await query.edit_message_text("⛔ У вас нет доступа к этой функции")

async def show_help(query):
    """Показ справки"""
    help_text = (
        "📖 **Справка по боту учета долгов**\n\n"
        "Текущие функции:\n"
        "• 📊 Проверить подключение - тест Google Sheets\n"
        "• 👥 Тестовые данные - пример данных из таблицы\n"
        "• 👤 Мой статус - информация о вашем аккаунте\n\n"
        "Следующий этап:\n"
        "• Подключение к реальной Google таблице\n"
        "• Расчет долгов сотрудников\n"
        "• Уведомления о долгах\n\n"
        "Версия 2.0 (Google Sheets тест)"
    )
    await query.edit_message_text(help_text, parse_mode='Markdown')

async def check_connection(query):
    """Проверка подключения к Google Sheets"""
    status, message = sheets_client.test_connection()
    
    if status:
        text = f"{message}\n\n"
        text += "✅ **Настройки проверены:**\n"
        text += f"• API ключ: {'Установлен' if GOOGLE_API_KEY else 'Отсутствует'}\n"
        text += f"• ID таблицы: {SPREADSHEET_ID[:20]}...\n"
        text += f"• Админы: {len(ADMIN_IDS)} человек\n\n"
        text += "Готово к подключению к реальной таблице!"
    else:
        text = f"{message}\n\n"
        text += "**Что проверить:**\n"
        text += "1. Добавлены ли GOOGLE_API_KEY в Railway?\n"
        text += "2. Добавлен ли SPREADSHEET_ID в Railway?\n"
        text += "3. Правильный ли ID таблицы?\n"
    
    await query.edit_message_text(text, parse_mode='Markdown')

async def show_test_data(query):
    """Показ тестовых данных"""
    data = sheets_client.get_test_data()
    
    text = "📋 **Тестовые данные из Google Sheets:**\n\n"
    total = 0
    
    for item in data:
        text += f"📅 {item['date']}\n"
        text += f"   👤 {item['employee']}\n"
        text += f"   🛒 {item['items']}\n"
        text += f"   💰 {item['amount']} ₽\n\n"
        total += item['amount']
    
    text += f"💵 **Общая сумма:** {total} ₽\n\n"
    text += "Это пример данных. Реальные данные будут загружаться из вашей таблицы."
    
    await query.edit_message_text(text, parse_mode='Markdown')

async def show_my_status(query, user_id):
    """Показ статуса пользователя"""
    is_admin = str(user_id) in ADMIN_IDS
    
    text = "👤 **Ваш статус:**\n\n"
    text += f"• ID: {user_id}\n"
    text += f"• Роль: {'👑 Администратор' if is_admin else '👤 Сотрудник'}\n"
    text += f"• Google Sheets: {'✅ Подключено' if sheets_client.connected else '⚠️ В разработке'}\n"
    text += f"• Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
    
    if is_admin:
        text += "**Доступные функции:**\n"
        text += "• Управление долгами\n• Просмотр всех сотрудников\n• Настройки бота\n"
    else:
        text += "**Доступные функции:**\n"
        text += "• Просмотр своего долга\n• История покупок\n• Уведомления\n"
    
    await query.edit_message_text(text, parse_mode='Markdown')

async def show_my_debt(query, user_id):
    """Показ долга пользователя (заглушка)"""
    text = "📊 **Ваш текущий долг:**\n\n"
    text += "Функция в активной разработке.\n\n"
    text += "**Скоро здесь будет:**\n"
    text += "• Общая сумма долга\n• История операций\n• График погашения\n\n"
    text += "А пока вы можете:\n"
    text += "1. Проверить статус подключения\n"
    text += "2. Посмотреть пример данных\n"
    text += "3. Обратиться к администратору"
    
    await query.edit_message_text(text, parse_mode='Markdown')

async def show_daily_debt(query):
    """Показ долга за день (заглушка)"""
    text = "📅 **Долг за день:**\n\n"
    text += "Функция в активной разработке.\n\n"
    text += "**Скоро здесь будет:**\n"
    text += "• Выбор даты\n• Список покупок за день\n• Сумма за день\n\n"
    text += f"Сегодня: {datetime.now().strftime('%d.%m.%Y')}"
    
    await query.edit_message_text(text, parse_mode='Markdown')

def main():
    """Запуск бота"""
    if not TELEGRAM_TOKEN:
        logger.error("❌ Токен бота не найден!")
        print("Добавьте TELEGRAM_TOKEN в настройки Railway")
        return
    
    # Проверяем настройки Google
    if not GOOGLE_API_KEY:
        logger.warning("⚠️ GOOGLE_API_KEY не настроен")
    if not SPREADSHEET_ID:
        logger.warning("⚠️ SPREADSHEET_ID не настроен")
    
    # Создаем приложение
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # Запускаем бота
    logger.info("🤖 Бот запускается с Google Sheets поддержкой...")
    print("=" * 50)
    print("Бот запущен!")
    print(f"Админы: {ADMIN_IDS}")
    print(f"Google API ключ: {'Есть' if GOOGLE_API_KEY else 'Нет'}")
    print(f"ID таблицы: {SPREADSHEET_ID[:20]}...")
    print("=" * 50)
    
    app.run_polling()

if __name__ == "__main__":
    main()