import os

# Reads from environment variables on GitHub Actions
# Falls back to hardcoded values when running locally
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', 'your-token-here')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 'your-chat-id-here')