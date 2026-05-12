import asyncio
from telegram import Bot
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

async def send_telegram_message(transaction):
    bot = Bot(token=TELEGRAM_TOKEN)
    
    # Determine emoji and label based on transaction type
    if transaction['type'] == 'debit':
        arrow = "📉"
        label = "Debit"
        sign = "-"
    elif transaction['type'] == 'credit':
        arrow = "📈"
        label = "Credit"
        sign = "+"
    else:
        arrow = "❓"
        label = "Unknown"
        sign = ""

    # Format the amount nicely with commas e.g 1800.00 → 1,800.00
    amount = f"{transaction['amount']:,.2f}"

    # Pull balance from email if available, else show N/A
    balance = transaction.get('balance', 'N/A')
    if isinstance(balance, float):
        balance = f"₦{balance:,.2f}"

    description = transaction.get('description') or 'Bank Transaction'
    # Escape special Markdown characters so Telegram doesn't misread them
import re
description = re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', description)

    message = (
        f"🏦 *FirstBank Alert*\n"
        f"─────────────────\n"
        f"{arrow} *{label}:* ₦{sign}{amount}\n"
        f"📝 {description}\n"
        f"💰 *Balance:* {balance}"
    )

    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=message,
        parse_mode='MarkdownV2'
    )
    print(f"Telegram notification sent: {label} ₦{amount}")

def notify(transaction):
    """Synchronous wrapper — called from read_emails.py"""
    asyncio.run(send_telegram_message(transaction))
