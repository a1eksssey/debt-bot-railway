import os

# ==================== НАСТРОЙКИ ====================

# 1. ТОКЕН ВАШЕГО TELEGRAM БОТА (берется из Railway)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")

# 2. API-КЛЮЧ GOOGLE
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyD0cn-AUn1GENBIZoZCkg1vdwiIpbdwBLQ")

# 3. ID ВАШЕЙ GOOGLE ТАБЛИЦЫ
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "19iUX_rF9jpsDv9p5V_nj9dapOO6zUR5GDzy9o5GGoI8")

# 4. ID АДМИНИСТРАТОРОВ
ADMIN_IDS = os.getenv("ADMIN_IDS", "283883536,222222222").split(',')

# 5. НАСТРОЙКИ УВЕДОМЛЕНИЙ
ENABLE_NOTIFICATIONS = True
ENABLE_LOGGING = True
NOTIFICATION_HOUR = 9

# ==================== ТЕХНИЧЕСКИЕ ====================
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']