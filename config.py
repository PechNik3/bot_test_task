import os

# Загрузка переменных окружения
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# Проверка наличия необходимых переменных окружения
if not TELEGRAM_API_TOKEN:
    raise ValueError("TELEGRAM_API_TOKEN is not set. Please set the API token in the environment variables.")
