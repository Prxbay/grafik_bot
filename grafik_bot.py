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

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот, готов к работе.")

# Обработка входящих сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Проверка на нужный префикс
    if not text.startswith(TARGET_PREFIX):
        return

    # Проверка на наличие строки с 3.2
    if TARGET_LINE_PREFIX not in text:
        return

    # Проверка на наличие месяца
    if not any(month in text.lower() for month in MONTHS):
        return

    # Пробуем найти дату (день + месяц)
    date_match = re.search(r"(\d{1,2})\s+(" + "|".join(MONTHS) + r")", text.lower())
    if date_match:
        day, month = date_match.groups()
        formatted_date = f"{day} {month}"
    else:
        formatted_date = "дату не удалось извлечь"

    # Формируем сообщение
    message = f"📌 Обнаружено сообщение с датой: {formatted_date}\n\n{text}"

    # Рассылаем всем получателям
    for user_id in RECIPIENTS:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"Ошибка при отправке {user_id}: {e}")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()