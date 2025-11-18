from telegram.ext import Updater, MessageHandler, Filters
import re

TOKEN = '8510553698:AAHNZDB-7q5LMw8BPpAjCM5hMgzQu5SkqpM'

# 📬 Список получателей
RECIPIENTS = [431330942, 337029691]

TARGET_PREFIX = "За командою НЕК"
TARGET_LINE_PREFIX = "3.2"

# 🗓️ Список украинских месяцев, которые бот будет ловить
MONTHS = ["листопада", "грудня"]

def handle_message(update, context):
    text = update.message.text

    if TARGET_PREFIX in text:
        # 🗓️ Ищем дату: "18 листопада", "1 грудня" и т.д.
        date_match = re.search(r'(\d{1,2})\s+(' + '|'.join(MONTHS) + r')', text)
        if date_match:
            day = date_match.group(1)
            month = date_match.group(2)
            date_text = f"{day} {month}"
        else:
            date_text = "дата не найдена"

        # 🔍 Ищем строку, начинающуюся с "3.2"
        for line in text.split('\n'):
            if line.strip().startswith(TARGET_LINE_PREFIX):
                response = f"На {date_text}:\n{line.strip()}"
                for user_id in RECIPIENTS:
                    context.bot.send_message(chat_id=user_id, text=response)
                break

def main():
    print("Бот запущен и слушает сообщения...")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()