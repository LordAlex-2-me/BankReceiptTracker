import os

# Reads from environment variables on GitHub Actions
# Falls back to hardcoded values when running locally
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '8798615404:AAEIneri_D6DExXo0Pp1SFW8V_NyQSiDz5c')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '6673920353')