import re
import time
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

# 🔐 Токен из переменной окружения
import os
TOKEN = os.getenv("TOKEN")

# 🎯 Настройки фильтра
TARGET_PREFIX = "За командою НЕК"
TARGET_LINE_PREFIX = "3.2"
MONTHS = [
    "січня", "лютого", "березня", "квітня", "травня", "червня",
    "липня", "серпня", "вересня", "жовтня", "листопада", "грудня"
]

# 👥 Кому отправлять
RECIPIENTS = [
    123456789, 987654321  # замените на реальные user_id
]

# 🧠 Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text

    if TARGET_PREFIX not in text:
        return
    if TARGET_LINE_PREFIX not in text:
        return
    if not any(month in text.lower() for month in MONTHS):
        return

    date_match = re.search(r"(\d{1,2})\s+(" + "|".join(MONTHS) + r")", text.lower())
    formatted_date = f"{date_match.group(1)} {date_match.group(2)}" if date_match else "дату не удалось извлечь"

    line_match = re.search(r"3\.2\s+([^\n\r]+)", text)
    line_times = line_match.group(1).strip() if line_match else "не удалось извлечь часи"

    message = f"🗓️ Дата: {formatted_date}\n💡 Часи: {line_times}"

    for user_id in RECIPIENTS:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"Ошибка при отправке {user_id}: {e}")

# 🚀 Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    print("Бот запущен")
    app.run_polling()

# 🧩 Фейковый цикл для Render (если нужно)
if __name__ == "__main__":
    main()
    while True:
        time.sleep(60)