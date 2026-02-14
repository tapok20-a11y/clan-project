from datetime import timedelta
import os

API_TOKEN = os.getenv("BOT_TOKEN", "8593325345:AAEYst2Ur-OmxMeDQqsVyT5KWvh7g8KSrkA")

# Ссылки для принятых участников
CHAT_LINKS = [
    "https://t.me/chat1",
    "https://t.me/chat2",
]
FORM_LINK = "https://example.com/form"

# Ограничения анкеты
MAX_AGE = 11
SESSION_TIMEOUT = timedelta(hours=12)

# Пути к данным
DB_PATH = os.getenv("DB_PATH", "bot_data.sqlite3")
LOG_FILE = os.getenv("ACCEPTED_LOG_FILE", "accepted.log")
PROFILES_DIR = os.getenv("PROFILES_DIR", "profiles")

# Веб-панель
WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")
WEB_PORT = int(os.getenv("WEB_PORT", "8000"))
