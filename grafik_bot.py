import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# 🔐 Токен бота
TOKEN = '8510553698:AAHNZDB-7q5LMw8BPpAjCM5hMgzQu5SkqpM'

# 📬 Список получателей
RECIPIENTS = [431330942, 337029691]

# 🎯 Целевые префиксы
TARGET_PREFIX = "За командою НЕК"
TARGET_LINE_PREFIX = "3.2"

# 🗓️ Украинские месяцы
MONTHS = ["листопада", "грудня"]

# ✅ Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот, готов к работе.")

# ✅ Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if not text.startswith(TARGET_PREFIX):
        return
    if TARGET_LINE_PREFIX not in text:
        return
    if not any(month in text.lower() for month in MONTHS):
        return

    date_match = re.search(r"(\d{1,2})\s+(" + "|".join(MONTHS) + r")", text.lower())
    if date_match:
        day, month = date_match.groups()
        formatted_date = f"{day} {month}"
    else:
        formatted_date = "дату не удалось извлечь"

    line_match = re.search(r"3\.2\s+([^\n\r]+)", text)
    if line_match:
        line_times = line_match.group(1).strip()
    else:
        line_times = "не удалось извлечь часи"

    message = f"🗓️ Дата: {formatted_date}\n💡 Часи: {line_times}"

    for user_id in RECIPIENTS:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"Ошибка при отправке {user_id}: {e}")

# ✅ Запуск
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()