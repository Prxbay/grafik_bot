# -*- coding: utf-8 -*-

import re
import time
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

# 🔐 Токен напрямую (если не используешь переменные окружения)
TOKEN = "8510553698:AAHNZDB-7q5LMw8BPpAjCM5hMgzQu5SkqpM"

# 👥 Список получателей
RECIPIENTS = [
    431330942, 337029691  # замени на реальные user_id
]

# 📅 Настройки фильтра
TARGET_PREFIX = "За командою НЕК"
TARGET_LINE_PREFIX = "3.2"
MONTHS = [
    "січня", "лютого", "березня", "квітня", "травня", "червня",
    "липня", "серпня", "вересня", "жовтня", "листопада", "грудня"
]

# 🧠 Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return

    text = msg.text

    if TARGET_PREFIX not in text:
        return
    if TARGET_LINE_PREFIX not in text:
        return
    if not any(month in text.lower() for month in MONTHS):
        return

    date_match = re.search(r"(\d{1,2})\s+(" + "|".join(MONTHS) + r")", text.lower())
    formatted_date = f"{date_match.group(1)} {date_match.group(2)}" if date_match else "дату не знайдено"

    line_match = re.search(r"3\.2\s+([^\n\r]+)", text)
    line_times = line_match.group(1).strip() if line_match else "часи не знайдено"

    message = f"🗓️ Дата: {formatted_date}\n💡 Часи: {line_times}"

    for user_id in RECIPIENTS:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"❌ Не вдалося надіслати {user_id}: {e}")

# 🚀 Запуск
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    print("✅ Бот запущено")
    app.run_polling()

# 🧩 Цикл для Render (если нужно)
if __name__ == "__main__":
    main()
    while True:
        time.sleep(60)