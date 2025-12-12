import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получаем токен из переменных окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "✅ Бот работает!\n"
        "Я успешно запущен на Railway!\n\n"
        "Ваш Telegram ID: " + str(update.effective_user.id)
    )

async def echo(update: Update, context):
    """Повторяет сообщение пользователя"""
    await update.message.reply_text(f"Вы сказали: {update.message.text}")

def main():
    """Запуск бота"""
    if not TOKEN:
        print("❌ Ошибка: Токен бота не найден!")
        print("Добавьте TELEGRAM_TOKEN в настройки Railway")
        return
    
    # Создаем приложение
    app = Application.builder().token(TOKEN).build()
    
    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Запускаем бота
    print("🤖 Бот запускается...")
    app.run_polling()

if __name__ == "__main__":
    main()